import random
from collections import deque
import numpy as np
import torch


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    
    def push(self, state, action, reward, next_state, done):
        """Add a new experience to the buffer."""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """Sample a batch of experiences from the buffer."""
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*batch)

        state = torch.tensor(np.stack(state), dtype=torch.float32)
        next_state = torch.tensor(np.stack(next_state), dtype=torch.float32)
        action = torch.tensor(action, dtype=torch.int64)
        reward = torch.tensor(reward, dtype=torch.float32)
        done = torch.tensor(done, dtype=torch.float32)

        return state, action, reward, next_state, done
    
    def __len__(self):
        """Return the current size of the buffer."""
        return len(self.buffer)