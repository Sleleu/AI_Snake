import pygame as pg
import random
from sklearn.neural_network import MLPRegressor
import numpy as np
from collections import deque


class SnakeAgent:
    
    def __init__(self, training=True):
        self.epsilon = 0.9 if training else 0
        self.learning_rate = 0.01
        self.gamma = 0.9
        self.reward = 0
        self.training = training

        self.state = None
        self.next_state = None
        self.reward = 0
        self.ACTIONS = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]
        self.state_size = 28
        
        self.Q_network = MLPRegressor(
            hidden_layer_sizes=(64, 64),
            activation="relu",
            solver="adam",
            learning_rate_init=self.learning_rate,
            random_state=42
        )
        dummy_states = np.zeros((1, self.state_size))
        dummy_targets = np.zeros((1, len(self.ACTIONS)))
        self.Q_network.fit(dummy_states, dummy_targets)
        
        self.replay_buffer = deque(maxlen=10000)
        self.batch_size = 64

    def select_action(self):
        if self.training and random.random() < self.epsilon:
            self.action = random.choice(self.ACTIONS)
        else:
            state = np.array(self.state).reshape(1, -1)
            Q_values = self.Q_network.predict(state)[0]
            self.action = self.ACTIONS[np.argmax(Q_values)]
        return self.action
    
    def update_policy(self):
        transition = (self.state, self.action, self.reward, self.next_state)
        self.replay_buffer.append(transition)
        
        batch = random.sample(self.replay_buffer, min(self.batch_size, len(self.replay_buffer)))
        states, actions, rewards, next_states = zip(*batch)
        
        states = np.array(states)
        next_states = np.array(next_states)
        
        current_Q_values = self.Q_network.predict(states)
        next_Q_values = self.Q_network.predict(next_states)
        max_next_Q = np.max(next_Q_values, axis=1)
        
        target_Q_values = current_Q_values.copy()
        for i, (action, reward) in enumerate(zip(actions, rewards)):
            action_idx = self.ACTIONS.index(action)
            target_Q_values[i, action_idx] = current_Q_values[i, action_idx] + \
                                             self.learning_rate * (
                                                 reward + 
                                                 self.gamma * max_next_Q[i] - 
                                                 current_Q_values[i, action_idx]
                                             )
        self.Q_network.partial_fit(states, target_Q_values)
        self.epsilon *= 0.9998