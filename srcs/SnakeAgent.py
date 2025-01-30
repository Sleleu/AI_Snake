import pygame as pg
import random
import pickle
from sklearn.neural_network import MLPRegressor
import numpy as np
from collections import deque
from .Colors import Colors as Col


class SnakeAgent:

    def __init__(self, training=True, model=None):
        self.epsilon = 0.9 if training else 0
        self.epsilon_min = 0.01
        self.learning_rate = 0.01
        self.gamma = 0.9
        self.reward = 0
        self.training = training
        self.model = model

        self.ACTIONS = [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]
        self.state_size = 16
        print(f"training of snakeAgent: {self.training}")
        print(f"Model loaded: {self.model}")
        if self.model:
            self.load_Q_network()
        else:
            self.create_Q_network()

        self.replay_buffer = deque(maxlen=50000)
        self.batch_size = 500

    def save_model(self, filename):
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.Q_network, f)
                print(f"Model saved as {filename}")
        except Exception as e:
            print(f"Error saving model: {e}")

    def load_Q_network(self):
        try:
            with open(self.model, "rb") as f:
                model_loaded = pickle.load(f)
                self.Q_network = model_loaded
                print("Model loaded successfully")
        except Exception as e:
            print(f"{Col.RED}{Col.BOLD}{e.__class__.__name__}: {e}{Col.END}")
            pg.quit()
            exit(1)
        return

    def create_Q_network(self):
        self.Q_network = MLPRegressor(
            hidden_layer_sizes=(256),
            activation="relu",
            solver="adam",
            learning_rate_init=self.learning_rate,
            random_state=42
        )
        dummy_states = np.zeros((1, self.state_size))
        dummy_targets = np.zeros((1, len(self.ACTIONS)))
        self.Q_network.fit(dummy_states, dummy_targets)

    def select_action(self, state):
        if self.training and random.random() < self.epsilon:
            action = random.choice(self.ACTIONS)
        else:
            state = np.array(state).reshape(1, -1)
            Q_values = self.Q_network.predict(state)[0]
            action = self.ACTIONS[np.argmax(Q_values)]
        return action

    def update_policy(self, state, next_state, action, reward):
        transition = (state, action, reward, next_state)
        self.replay_buffer.append(transition)

        batch = random.sample(self.replay_buffer,
                              min(self.batch_size, len(self.replay_buffer)))
        states, actions, rewards, next_states = zip(*batch)

        states = np.array(states)
        next_states = np.array(next_states)

        current_Q_values = self.Q_network.predict(states)
        next_Q_values = self.Q_network.predict(next_states)
        max_next_Q = np.max(next_Q_values, axis=1)

        target_Q_values = current_Q_values.copy()
        for i, (action, reward) in enumerate(zip(actions, rewards)):
            action_idx = self.ACTIONS.index(action)
            target_Q_values[i, action_idx] = \
                current_Q_values[i, action_idx] + self.learning_rate * (
                    reward
                    + self.gamma
                    * max_next_Q[i]
                    - current_Q_values[i, action_idx]
                    )
        if self.training:
            self.Q_network.partial_fit(states, target_Q_values)
            if self.epsilon > self.epsilon_min:
                self.epsilon *= 0.999
