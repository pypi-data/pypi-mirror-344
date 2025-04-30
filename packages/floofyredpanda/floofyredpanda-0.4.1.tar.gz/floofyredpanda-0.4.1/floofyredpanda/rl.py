# rl.py

import random
import numpy as np
from collections import deque

import torch
import torch.nn as nn
import torch.optim as optim


class DQN(nn.Module):
    """
    Simple feed-forward network for Q-value approximation.
    """

    def __init__(self, state_size, action_size, hidden_sizes=(64, 64)):
        super().__init__()
        layers = []
        input_dim = state_size
        for h in hidden_sizes:
            layers.append(nn.Linear(input_dim, h))
            layers.append(nn.ReLU())
            input_dim = h
        layers.append(nn.Linear(input_dim, action_size))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


class DQNAgent:
    """
    DQN Agent with memory replay.
    """

    def __init__(
            self,
            state_size,
            action_size,
            memory_size=2000,
            batch_size=64,
            gamma=0.95,
            lr=1e-3,
            eps_start=1.0,
            eps_min=0.01,
            eps_decay=0.995,
            device=None
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size
        self.gamma = gamma
        self.epsilon = eps_start
        self.eps_min = eps_min
        self.eps_decay = eps_decay

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQN(state_size, action_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """
        Epsilon-greedy action selection.
        """
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        state_v = torch.FloatTensor(state).to(self.device)
        qvals = self.model(state_v).detach().cpu().numpy()
        return int(np.argmax(qvals))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states_v = torch.FloatTensor(states).to(self.device)
        next_v = torch.FloatTensor(next_states).to(self.device)
        rewards_v = torch.FloatTensor(rewards).to(self.device)
        actions_v = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        dones_v = torch.FloatTensor(dones).to(self.device)

        # current Q
        q_vals = self.model(states_v).gather(1, actions_v).squeeze(1)
        # target Q
        next_max = self.model(next_v).max(1)[0]
        expected = rewards_v + self.gamma * next_max * (1 - dones_v)

        loss = self.loss_fn(q_vals, expected.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # decay epsilon
        if self.epsilon > self.eps_min:
            self.epsilon *= self.eps_decay

    def save(self, path):
        torch.save({
            'model_state': self.model.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
        }, path)

    def load(self, path):
        chk = torch.load(path, map_location=self.device)
        self.model.load_state_dict(chk['model_state'])
        self.optimizer.load_state_dict(chk['optimizer_state'])
        self.epsilon = chk.get('epsilon', self.epsilon)


def rl(input1, RLpoints, agent=None):
    """
    Trains (or continues training) a DQN agent.

    Args:
      input1   : an OpenAI-Gym-style env (must have .reset() and .step()).
      RLpoints : int, number of episodes to train for.
      agent    : optional DQNAgent; if None, a fresh one is created.

    Returns:
      DQNAgent : your trained (or further trained) agent.
    """
    env = input1
    # determine sizes from gym
    sample_state = env.reset()
    if isinstance(sample_state, tuple):  # some envs return (obs, info)
        sample_state = sample_state[0]
    state_size = np.prod(sample_state.shape)
    action_size = env.action_space.n

    if agent is None:
        agent = DQNAgent(state_size, action_size)

    for ep in range(1, RLpoints + 1):
        state = env.reset()
        if isinstance(state, tuple):
            state = state[0]
        state = state.reshape(1, -1)

        done = False
        while not done:
            action = agent.act(state)
            nxt, reward, done, _ = env.step(action)
            if isinstance(nxt, tuple):
                nxt = nxt[0]
            nxt = nxt.reshape(1, -1)

            agent.memorize(state, action, reward, nxt, done)
            state = nxt
            agent.replay()

    return agent

def predict(agent, state):
    """
    Run a single state through the agent and get the best action.
    """
    state = torch.FloatTensor(state).unsqueeze(0).to(agent.device)
    qvals = agent.model(state).detach().cpu().numpy()
    return int(np.argmax(qvals))
