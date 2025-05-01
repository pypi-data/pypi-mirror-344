# rl.py
import random
from collections import deque
from typing import Tuple, Union, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class ReplayBuffer:
    """Simple FIFO replay buffer; swap in your PER if you like."""
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, transition: Tuple):
        self.buffer.append(transition)

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        return map(np.vstack, zip(*batch))

    def __len__(self):
        return len(self.buffer)


class DQN(nn.Module):
    """
    Feed-forward Q-network. Switch on dueling to get Value/Advantage heads.
    """
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_sizes: Tuple[int, ...] = (64, 64),
        dueling: bool = False
    ):
        super().__init__()
        self.dueling = dueling

        # common trunk
        layers = []
        in_dim = state_dim
        for h in hidden_sizes:
            layers += [nn.Linear(in_dim, h), nn.ReLU()]
            in_dim = h
        self.trunk = nn.Sequential(*layers)

        if not dueling:
            self.head = nn.Linear(in_dim, action_dim)
        else:
            # dueling: separate advantage and value streams
            self.adv = nn.Linear(in_dim, action_dim)
            self.val = nn.Linear(in_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.trunk(x)
        if not self.dueling:
            return self.head(x)
        adv = self.adv(x)
        val = self.val(x)
        # combine into Q-values: Q = V + (A - mean(A))
        return val + adv - adv.mean(dim=1, keepdim=True)


class DQNAgent:
    """
    DQN agent supporting:
      • optional target network
      • Double-DQN
      • dueling architecture
      • soft or hard target updates
      • gradient clipping
      • replay buffer (swap in PER if desired)
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
        tau: float = 1.0,             # 1.0 = hard update, <1 for soft
        double_dqn: bool = False,
        dueling: bool = False,
        grad_clip: Optional[float] = None,
        device: Optional[Union[str, torch.device]] = None,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Q-networks
        self.model = DQN(state_size, action_size, hidden_sizes, dueling).to(self.device)
        self.target = None
        if use_target_net:
            self.target = DQN(state_size, action_size, hidden_sizes, dueling).to(self.device)
            self.target.load_state_dict(self.model.state_dict())
            self.target.eval()

        self.double_dqn = double_dqn
        self.gamma = gamma

        # ε-greedy
        self.epsilon = eps_start
        self.eps_min = eps_min
        self.eps_decay = eps_decay

        # optimiser & loss
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
        self.grad_clip = grad_clip

        # replay buffer
        self.buffer = ReplayBuffer(memory_size)
        self.batch_size = batch_size

        # target update
        self.use_target = use_target_net
        self.tau = tau
        self.update_freq = target_update_freq
        self.step_counter = 0

    def act(self, state: np.ndarray) -> int:
        """ε-greedy action selection."""
        if random.random() < self.epsilon:
            return random.randrange(self.model.net[-1].out_features)
        state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            qvals = self.model(state_t)
        return int(qvals.argmax(dim=1).item())

    def store(self, s, a, r, s_next, done):
        self.buffer.push((s, [a], [r], s_next, [done]))

    def _compute_targets(self, rewards, next_states, dones):
        # Q(s', a') by behaviour or target net
        with torch.no_grad():
            if self.double_dqn and self.use_target:
                best_actions = self.model(next_states).argmax(dim=1, keepdim=True)
                next_q = self.target(next_states).gather(1, best_actions).squeeze(1)
            elif self.use_target:
                next_q = self.target(next_states).max(1)[0]
            else:
                next_q = self.model(next_states).max(1)[0]
        return rewards + self.gamma * next_q * (1 - dones)

    def learn(self):
        """Sample from buffer and do a DQN update."""
        if len(self.buffer) < self.batch_size:
            return

        s, a, r, s_next, d = self.buffer.sample(self.batch_size)
        states      = torch.FloatTensor(s).to(self.device)
        actions     = torch.LongTensor(a).to(self.device)
        rewards     = torch.FloatTensor(r).squeeze(1).to(self.device)
        next_states = torch.FloatTensor(s_next).to(self.device)
        dones       = torch.FloatTensor(d).squeeze(1).to(self.device)

        # current Q
        q_vals = self.model(states).gather(1, actions).squeeze(1)
        # target Q
        q_target = self._compute_targets(rewards, next_states, dones)

        loss = self.loss_fn(q_vals, q_target)
        self.optimizer.zero_grad()
        loss.backward()

        if self.grad_clip:
            nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)

        self.optimizer.step()

        # ε decay
        if self.epsilon > self.eps_min:
            self.epsilon *= self.eps_decay

        # update target net
        if self.use_target:
            self.step_counter += 1
            if self.tau < 1.0:
                # soft update
                for p, tp in zip(self.model.parameters(), self.target.parameters()):
                    tp.data.copy_(tp.data * (1 - self.tau) + p.data * self.tau)
            elif self.step_counter % self.update_freq == 0:
                # hard update
                self.target.load_state_dict(self.model.state_dict())

    def save(self, path: str):
        ckpt = {
            'model':     self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon':   self.epsilon
        }
        if self.use_target:
            ckpt['target'] = self.target.state_dict()
        torch.save(ckpt, path)

    def load(self, path: str):
        ckpt = torch.load(path, map_location=self.device)
        self.model.load_state_dict(ckpt['model'])
        self.optimizer.load_state_dict(ckpt['optimizer'])
        self.epsilon = ckpt.get('epsilon', self.epsilon)
        if self.use_target and 'target' in ckpt:
            self.target.load_state_dict(ckpt['target'])


def train(
    env,
    episodes: int = 500,
    agent: Optional[DQNAgent] = None,
    **agent_kwargs
) -> DQNAgent:
    """
    Train a DQNAgent for given episodes.
    Pass agent_kwargs to enable advanced features, e.g.:
      use_target_net=True, double_dqn=True, dueling=True, grad_clip=1.0
    """
    # infer dims
    sample = env.reset()
    if isinstance(sample, tuple):
        sample = sample[0]
    state_dim = int(np.prod(sample.shape))
    action_dim = env.action_space.n

    if agent is None:
        agent = DQNAgent(state_dim, action_dim, **agent_kwargs)

    for ep in range(1, episodes + 1):
        obs = env.reset()
        if isinstance(obs, tuple):
            obs = obs[0]
        state = obs.reshape(-1)

        done = False
        while not done:
            a = agent.act(state)
            nxt, r, done, _ = env.step(a)
            nxt = nxt[0] if isinstance(nxt, tuple) else nxt
            next_state = nxt.reshape(-1)

            agent.store(state, a, r, next_state, done)
            agent.learn()
            state = next_state

    return agent


def predict(agent: DQNAgent, state: np.ndarray) -> int:
    """Quick inference: best action for a single state."""
    return agent.act(state)
rl = train