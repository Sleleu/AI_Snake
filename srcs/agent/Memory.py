import numpy as np
import torch

class Memory:
    """Experience replay buffer using numpy arrays.

    Args:
        `memory_size`: Maximum size of buffer
        `device`: Device to store tensors (cuda/cpu)

    Implementation:
        Uses np arrays as circular buffers to store transitions:
        - states[memory_size, state_size]
        - actions[memory_size]
        - rewards[memory_size]
        - next_states[memory_size, state_size]
        - dones[memory_size]

        New entries overwrite oldest when full.
    """
    def __init__(self, memory_size: int, device: torch.device):
        self.device = device
        self.memory_size = memory_size
        self.position = 0
        self.size = 0

        self.states = np.zeros((memory_size, 20), dtype=np.float32)
        self.actions = np.zeros(memory_size, dtype=np.int64)
        self.rewards = np.zeros(memory_size, dtype=np.float32)
        self.next_states = np.zeros((memory_size, 20), dtype=np.float32)
        self.dones = np.zeros(memory_size, dtype=np.float32)

    def push(self,
             state: list,
             action: int,
             reward: float,
             next_state: list,
             done: bool
             ) -> None:
        """Add transition to circular buffer, overwriting oldest if full.

        Args:
            `state`: Current state vector
            `action`: Action taken (0-3)
            `reward`: Reward received
            `next_state`: Next state vector
            `done`: Whether episode ended
        """
        self.states[self.position] = np.array(state)
        self.actions[self.position] = action
        self.rewards[self.position] = reward
        self.next_states[self.position] = np.array(next_state)
        self.dones[self.position] = done

        self.position = (self.position + 1) % self.memory_size
        self.size = min(self.size + 1, self.memory_size)

    def sample(self, batch_size: int) -> tuple[torch.Tensor]:
        """Sample random batch of transitions.

        Args:
            `batch_size`: Number of transitions to sample

        Returns:
            `tuple`: (states, actions, rewards, next_states, dones) as tensors
        """
        i: np.ndarray = np.random.choice(self.size, batch_size)
        return (
            torch.FloatTensor(self.states[i]).to(self.device),
            torch.LongTensor(self.actions[i]).to(self.device),
            torch.FloatTensor(self.rewards[i]).to(self.device),
            torch.FloatTensor(self.next_states[i]).to(self.device),
            torch.FloatTensor(self.dones[i]).to(self.device)
        )

    def __len__(self) -> int:
        """Return current size of the replay buffer."""
        return self.size