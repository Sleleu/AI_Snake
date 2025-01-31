import random
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class QNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, state):
        hidden = F.relu(self.fc1(state))
        q_values = self.fc2(hidden)
        return q_values
    
class Memory:
    def __init__(self, memory_size):
        self.buffer = deque(maxlen=memory_size)
    
    def push(self, state, action, reward, next_state, done):
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)
    
    def sample(self, batch_size):
        batch_size = min(batch_size, len(self.buffer))
        batch = random.sample(list(self.buffer), batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        return states, actions, rewards, next_states, dones
    
    def __len__(self):
        return len(self.buffer)


class SnakeAgent:
    def __init__(self, training=True, model=None):
        self.epsilon = 0.9 if training else 0
        self.epsilon_min = 0.001
        
        self.lr = 0.001
        self.gamma = 0.9
        self.batch_size = 100
        
        self.model = QNetwork(16, 256, 4)
        self.memory = Memory(100_000)
        self.criterion = nn.MSELoss()
        
        if model:
            self.load_model(model)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state)
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
            next_Q_values = self.model(next_states)
        max_Q_values = next_Q_values.max(1)[0]
        # Q(s,a) = R + γ * max(Q(s',a')) / add (1 - dones) for terminal state
        targets = rewards + self.gamma * max_Q_values * (1 - dones)
        
        loss = self.criterion(predictions.squeeze(-1), targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.epsilon = max(self.epsilon_min, self.epsilon * 0.995)

    def update(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)
        self.learn()

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        self.model.eval()
    
    def save_model(self, path):
        torch.save(self.model.state_dict(), path)
