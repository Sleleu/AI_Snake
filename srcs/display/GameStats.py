from ..game.SnakeGame import SnakeGame
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


class GameStats:
    def __init__(self):
        self.episode_lengths = []
        self.records = []

        self.max_length = 0
        self.total_episodes = 0

        self.moving_avg_window = 20
        self.start_time = datetime.now()

    def get_stats(self, snake_game: SnakeGame):
        self.total_episodes = snake_game.episode
        current_length = len(snake_game.snake)
        self.episode_lengths.append(current_length)
        self.agent_epsilon = snake_game.snakeAgent.epsilon

        if current_length > self.max_length:
            self.max_length = current_length
        self.records.append(self.max_length)

        self.print_periodic_stats()
        if snake_game.save and self.total_episodes % 100 == 0 and self.total_episodes > 0:
            self.plot_statistics(snake_game.save)

    def print_periodic_stats(self) -> None:
        if self.total_episodes % 100 == 0 and self.total_episodes > 0:
            avg_length = np.mean(self.episode_lengths[-100:])
            elapsed_time = datetime.now() - self.start_time

            print(f"\n=== Episode stats {self.total_episodes} ===")
            print(f"Time elapsed: {elapsed_time}")
            print(f"Mean Length (100 last): {avg_length:.2f}")
            print(f"Length Record: {self.max_length}")
            print(f"Agent epsilon: {self.agent_epsilon}")
            print("=====================================\n")

    def plot_statistics(self, save_path):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Length evolution
        episodes = range(len(self.episode_lengths))
        ax1.plot(episodes, self.episode_lengths, label='Length per episode', alpha=0.3)
        ax1.plot(episodes[self.moving_avg_window-1:],
                 self.calculate_moving_average(self.episode_lengths),
                 label=f'Moving mean ({self.moving_avg_window} episodes)',
                 linewidth=2)
        ax1.set_title('Snake length evolution')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Length')
        ax1.legend()

        # Record evolution
        ax2.plot(episodes, self.records, label='Record evolution', color='red')
        ax2.set_title('Record evolution')
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Record')
        ax2.legend()

        plt.tight_layout()
        plt.savefig(f"{save_path}/stats.png")
        plt.close()

    def calculate_moving_average(self, data):
        return [np.mean(data[i-self.moving_avg_window:i])
                for i in range(self.moving_avg_window, len(data)+1)]
