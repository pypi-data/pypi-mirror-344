import random
import logging
from collections import deque
from typing import Tuple, Union, Optional, Type, Dict, Any, List

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import _LRScheduler


def set_seed(seed: int) -> None:
    """Set global seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


class ReplayBuffer:
    """Simple FIFO replay buffer; swap in your PER if you like."""
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, transition: Tuple):
        """Add a transition (s, a, r, s_next, done)."""
        self.buffer.append(transition)

    def sample(self, batch_size: int) -> Tuple:
        batch = random.sample(self.buffer, batch_size)
        return map(np.vstack, zip(*batch))

    def __len__(self) -> int:
        return len(self.buffer)


class PrioritizedReplayBuffer(ReplayBuffer):
    """Prioritized Experience Replay (PER) with proportional prioritization."""
    def __init__(self, capacity: int = 10000, alpha: float = 0.6, beta: float = 0.4):
        super().__init__(capacity)
        self.alpha = alpha
        self.beta = beta
        self.priorities = deque(maxlen=capacity)

    def push(self, transition: Tuple):
        super().push(transition)
        # new transition gets max priority
        max_prio = max(self.priorities) if self.priorities else 1.0
        self.priorities.append(max_prio)

    def sample(self, batch_size: int):
        prios = np.array(self.priorities, dtype=np.float32)
        probs = prios ** self.alpha
        probs /= probs.sum()
        indices = np.random.choice(len(self.buffer), batch_size, p=probs)
        samples = [self.buffer[idx] for idx in indices]
        weights = (len(self.buffer) * probs[indices]) ** (-self.beta)
        weights /= weights.max()
        # convert to numpy batches
        transitions = tuple(map(np.vstack, zip(*samples)))
        # transitions: (states, actions, rewards, next_states, dones)
        return (*transitions, indices, weights)

    def update_priorities(self, indices: List[int], errors: np.ndarray) -> None:
        """Update priorities of sampled transitions."""
        for idx, err in zip(indices, errors):
            self.priorities[idx] = abs(err) + 1e-6

class DQN(nn.Module):
    """Feed-forward Q-network; switch on dueling for Value/Advantage heads."""
    def __init__(self,
                 state_dim: int,
                 action_dim: int,
                 hidden_sizes: Tuple[int, ...] = (64, 64),
                 dueling: bool = False):
        super().__init__()
        self.dueling = dueling
        layers = []
        in_dim = state_dim
        for h in hidden_sizes:
            layers.extend([nn.Linear(in_dim, h), nn.ReLU(inplace=True)])
            in_dim = h
        self.trunk = nn.Sequential(*layers)
        if not dueling:
            self.head = nn.Linear(in_dim, action_dim)
        else:
            self.adv = nn.Linear(in_dim, action_dim)
            self.val = nn.Linear(in_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.trunk(x)
        if not self.dueling:
            return self.head(x)
        adv = self.adv(x)
        val = self.val(x)
        return val + adv - adv.mean(dim=1, keepdim=True)


class DQNAgent:
    """
    DQN agent with options:
      • target network (hard/soft updates)
      • Double-DQN
      • dueling
      • gradient clipping
      • configurable replay buffer
      • LR scheduler support
      • evaluation helper
    """
    def __init__(
        self,
        state_size: int,
        action_size: int,
        hidden_sizes: Tuple[int, ...] = (64, 64),
        lr: float = 1e-3,
        gamma: float = 0.99,
        eps_start: float = 1.0,
        eps_min: float = 0.01,
        eps_decay: float = 0.995,
        memory_size: int = 10000,
        batch_size: int = 64,
        use_target_net: bool = False,
        target_update_freq: int = 1000,
        tau: float = 1.0,
        double_dqn: bool = False,
        dueling: bool = False,
        grad_clip: Optional[float] = None,
        device: Optional[str] = None,
        buffer_class: Type[ReplayBuffer] = ReplayBuffer,
        buffer_kwargs: Optional[Dict[str, Any]] = None,
        scheduler_class: Optional[Type[_LRScheduler]] = None,
        scheduler_kwargs: Optional[Dict[str, Any]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.logger = logger or logging.getLogger(__name__)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = eps_start
        self.eps_min = eps_min
        self.eps_decay = eps_decay

        # networks
        self.model = DQN(state_size, action_size, hidden_sizes, dueling).to(self.device)
        self.use_target = use_target_net
        if self.use_target:
            self.target = DQN(state_size, action_size, hidden_sizes, dueling).to(self.device)
            self.target.load_state_dict(self.model.state_dict())
            self.target.eval()
        else:
            self.target = None
        self.double_dqn = double_dqn

        # optimizer & scheduler
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        if scheduler_class:
            params = scheduler_kwargs or {}
            self.scheduler = scheduler_class(self.optimizer, **params)
        else:
            self.scheduler = None
        self.loss_fn = nn.MSELoss()
        self.grad_clip = grad_clip

        # replay buffer
        buf_args = buffer_kwargs or {}
        self.buffer = buffer_class(memory_size, **buf_args)
        self.batch_size = batch_size

        # target updates
        self.tau = tau
        self.update_freq = target_update_freq
        self.step_counter = 0

        # metrics
        self.last_loss: Optional[float] = None
        self.total_steps = 0

    def __repr__(self) -> str:
        return (f"<DQNAgent(s={self.state_size}, a={self.action_size}, eps={self.epsilon:.3f}, "
                f"gamma={self.gamma}, device={self.device})>")

    def act(self, state: np.ndarray) -> int:
        """ε-greedy action selection."""
        if random.random() < self.epsilon:
            action = random.randint(0, self.action_size - 1)
        else:
            state_t = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
            with torch.no_grad():
                qvals = self.model(state_t)
            action = int(qvals.argmax(dim=1).item())
        self.logger.debug(f"Action: {action}, eps={self.epsilon:.3f}")
        return action

    def store(self, s: np.ndarray, a: int, r: float, s_next: np.ndarray, done: bool) -> None:
        """Push transition into replay buffer."""
        self.buffer.push((s, [a], [r], s_next, [done]))

    def learn(self) -> None:
        """Perform one training step if enough samples are available."""
        if len(self.buffer) < self.batch_size:
            return

        batch = self.buffer.sample(self.batch_size)
        # PER returns extra indices/weights
        if isinstance(self.buffer, PrioritizedReplayBuffer):
            s, a, r, s_next, d, idxs, weights = batch
            weights_t = torch.FloatTensor(weights).to(self.device)
        else:
            s, a, r, s_next, d = batch
            weights_t = None

        states = torch.FloatTensor(s).to(self.device)
        actions = torch.LongTensor(a).to(self.device)
        rewards = torch.FloatTensor(r).squeeze(1).to(self.device)
        next_states = torch.FloatTensor(s_next).to(self.device)
        dones = torch.FloatTensor(d).squeeze(1).to(self.device)

        q_vals = self.model(states).gather(1, actions).squeeze(1)
        with torch.no_grad():
            if self.double_dqn and self.target is not None:
                best_a = self.model(next_states).argmax(dim=1, keepdim=True)
                next_q = self.target(next_states).gather(1, best_a).squeeze(1)
            elif self.target is not None:
                next_q = self.target(next_states).max(1)[0]
            else:
                next_q = self.model(next_states).max(1)[0]
            q_target = rewards + self.gamma * next_q * (1 - dones)

        if weights_t is not None:
            loss = (weights_t * (q_vals - q_target).pow(2)).mean()
        else:
            loss = self.loss_fn(q_vals, q_target)
        self.last_loss = loss.item()

        self.optimizer.zero_grad()
        loss.backward()
        if self.grad_clip is not None:
            nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
        self.optimizer.step()
        if self.scheduler:
            self.scheduler.step()

        if isinstance(self.buffer, PrioritizedReplayBuffer):
            errors = (q_vals - q_target).abs().detach().cpu().numpy()
            self.buffer.update_priorities(idxs, errors)

        # epsilon decay
        self.epsilon = max(self.eps_min, self.epsilon * self.eps_decay)

        # target net update
        if self.target is not None:
            self.step_counter += 1
            if self.tau < 1.0:
                for p, tp in zip(self.model.parameters(), self.target.parameters()):
                    tp.data.copy_(tp.data * (1 - self.tau) + p.data * self.tau)
            elif self.step_counter % self.update_freq == 0:
                self.target.load_state_dict(self.model.state_dict())

        self.total_steps += 1
        self.logger.debug(f"Step {self.total_steps}, Loss: {self.last_loss:.6f}")

    def evaluate(self, env, episodes: int = 10) -> float:
        """Run episodes without exploration to get avg reward."""
        total, orig_eps = 0.0, self.epsilon
        self.epsilon = 0.0
        for _ in range(episodes):
            obs = env.reset()
            if isinstance(obs, tuple): obs = obs[0]
            state = obs.reshape(-1)
            done = False
            while not done:
                action = self.act(state)
                nxt, r, done, _ = env.step(action)
                nxt = nxt[0] if isinstance(nxt, tuple) else nxt
                state = nxt.reshape(-1)
                total += r
        self.epsilon = orig_eps
        avg = total / episodes
        self.logger.info(f"Eval: {avg:.2f} over {episodes} eps")
        return avg

    def save(self, path: str) -> None:
        """Save model, optimizer, eps, and hyperparams."""
        data = {
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'hyperparams': {k: getattr(self, k) for k in ['gamma', 'eps_min', 'eps_decay']}
        }
        if self.target is not None:
            data['target'] = self.target.state_dict()
        torch.save(data, path)
        self.logger.info(f"Checkpoint saved to {path}")

    def load(self, path: str) -> None:
        """Load checkpoint from disk."""
        chk = torch.load(path, map_location=self.device)
        self.model.load_state_dict(chk['model'])
        self.optimizer.load_state_dict(chk['optimizer'])
        self.epsilon = chk.get('epsilon', self.epsilon)
        if self.target is not None and 'target' in chk:
            self.target.load_state_dict(chk['target'])
        self.logger.info(f"Checkpoint loaded from {path}")


def train(
    env,
    episodes: int = 500,
    agent: Optional[DQNAgent] = None,
    **agent_kwargs
) -> DQNAgent:
    """
    Train a DQNAgent for a set number of episodes.
    Pass agent_kwargs to enable features like:
      use_target_net=True, double_dqn=True, dueling=True,
      grad_clip=1.0, buffer_class=PrioritizedReplayBuffer, scheduler_class=...
    """
    sample = env.reset()
    if isinstance(sample, tuple): sample = sample[0]
    state_dim = int(np.prod(sample.shape))
    action_dim = env.action_space.n
    if agent is None:
        agent = DQNAgent(state_dim, action_dim, **agent_kwargs)

    for ep in range(1, episodes + 1):
        obs = env.reset()
        if isinstance(obs, tuple): obs = obs[0]
        state = obs.reshape(-1)
        done = False
        ep_reward = 0.0
        while not done:
            a = agent.act(state)
            nxt, r, done, _ = env.step(a)
            nxt = nxt[0] if isinstance(nxt, tuple) else nxt
            next_state = nxt.reshape(-1)
            agent.store(state, a, r, next_state, done)
            agent.learn()
            state = next_state
            ep_reward += r
        agent.logger.info(f"Episode {ep}: Reward={ep_reward:.2f}")
    return agent


def predict(agent: DQNAgent, state: np.ndarray) -> int:
    """Quick inference: best action for a single state."""
    return agent.act(state)
