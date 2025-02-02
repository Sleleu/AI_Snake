import random
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class QNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, output_size)
        self.to(self.device)
        
    def forward(self, state):
        if not isinstance(state, torch.Tensor):
            state = torch.FloatTensor(state)
        state = state.to(self.device)
        hidden = F.relu(self.fc1(state))
        hidden = F.relu(self.fc2(hidden))
        q_values = self.fc3(hidden)
        return q_values
    
class Memory:
    def __init__(self, memory_size, device):
        self.buffer = deque(maxlen=memory_size)
        self.device = device
    
    def push(self, state, action, reward, next_state, done):
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size):
        batch_size = min(batch_size, len(self.buffer))
        batch = random.sample(list(self.buffer), batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)
        
        return states, actions, rewards, next_states, dones
    
    def __len__(self):
        return len(self.buffer)


class SnakeAgent:
    def __init__(self, training=True, model=None):
        self.epsilon = 0.9 if training else 0
        self.epsilon_min = 0.05
        
        self.lr = 0.0005
        self.gamma = 0.90
        self.batch_size = 1000

        # Q-Network
        self.model = QNetwork(20, 128, 4)
        
        self.training = training
        if self.training:
            # Target-Network
            self.target_model = QNetwork(20, 128, 4)
            # We copy initial weights/bias
            self.target_model.load_state_dict(self.model.state_dict())
            self.target_update_freq = 2000
            self.steps = 0
            
            self.memory = Memory(100_000, self.model.device)
            self.criterion = nn.MSELoss()
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        if model:
            self.load_model(model)

    def get_action(self, state, debug):
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state)
            if debug:
                print(f"QVALUES: {q_values}")
                print(f"Index delected: {q_values.argmax().item()}")
            return q_values.argmax().item()

    def learn(self):
        if len(self.memory) < self.batch_size:
            return
        
        # get a sample[batch_size] of experiences
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        # get q_values of each action taken in the sample
        Q_values = self.model(states)
        predictions = Q_values.gather(1, actions.unsqueeze(1))
        
        with torch.no_grad():
            next_Q_values = self.target_model(next_states)
        max_Q_values = next_Q_values.max(1)[0]
        # Q(s,a) = R + γ * max(Q(s',a')) / add (1 - dones) for terminal state
        targets = rewards + self.gamma * max_Q_values * (1 - dones)
        
        loss = self.criterion(predictions.squeeze(-1), targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.steps += 1
        if self.steps % self.target_update_freq == 0:
            self.target_model.load_state_dict(self.model.state_dict())

        self.epsilon = max(self.epsilon_min, self.epsilon * 0.998)

    def update(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)
        self.learn()

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()
    
    def save_model(self, path):
        torch.save(self.model.state_dict(), path)
