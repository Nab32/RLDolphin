import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from dqn import DQN
from replayBuffer import ReplayBuffer
from constants import ACTIONS


class Agent:
    def __init__(
        self,
        input_shape=(4, 210, 210),
        num_actions=len(ACTIONS),
        buffer_capacity=5000,
        batch_size=16,
        gamma=0.99,
        lr=1e-4,
        target_update_freq=1000,
        device=None
    ):
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.policy_net = DQN(input_shape, num_actions).to(self.device)
        self.target_net = DQN(input_shape, num_actions).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.replay_buffer = ReplayBuffer(capacity=buffer_capacity)

        self.batch_size = batch_size
        self.gamma = gamma
        self.num_actions = num_actions
        self.target_update_freq = target_update_freq
        self.step_counter = 0

        self.epsilon_start = 1.0
        self.epsilon_end = 0.05
        self.epsilon_decay = 25_000
        self.total_steps = 0

    def select_action(self, state):
        self.total_steps += 1

        epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * \
                  np.exp(-1.0 * self.total_steps / self.epsilon_decay)

        epsilon = 0.25
        print(f"Current epsilon: {epsilon:.4f}")
        if np.random.rand() < epsilon:
            return np.random.randint(0, self.num_actions)
        else:
            state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
            with torch.no_grad():
                q_values = self.policy_net(state)
                return q_values.argmax().item()

    def store_transition(self, state, action, reward, next_state, done):
    # Ensure no GPU/computation graph references
        state = np.array(state, dtype=np.float32)
        next_state = np.array(next_state, dtype=np.float32)
        action = int(action)
        reward = float(reward)
        done = float(done)  # Storing as float helps in torch calculations

        self.replay_buffer.push(state, action, reward, next_state, done)

    def train_step(self):
        if len(self.replay_buffer) < self.batch_size:
            print("Not enough samples in replay buffer to perform training step.")
            print(f"Current buffer size: {len(self.replay_buffer)}")
            return

        print(self.replay_buffer.__len__())
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

        states = torch.tensor(states, dtype=torch.float32, device=self.device)
        actions = torch.tensor(actions, dtype=torch.int64, device=self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32, device=self.device)
        dones = torch.tensor(dones, dtype=torch.float32, device=self.device)

        q_values = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            max_next_q = self.target_net(next_states).max(1)[0]
            target_q = rewards + (1 - dones) * self.gamma * max_next_q

        loss = nn.SmoothL1Loss()(q_values, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.step_counter += 1
        if self.step_counter % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        torch.cuda.empty_cache()

    def save(self, path):
        torch.save(self.policy_net.state_dict(), path)

    def load(self, path):
        self.policy_net.load_state_dict(torch.load(path))
        self.target_net.load_state_dict(self.policy_net.state_dict())