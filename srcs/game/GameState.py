from ..display.Colors import Colors as Col
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

class GameState:
    """Manages the game's state and control settings.

    Args:
        `is_ai_control`: Whether AI controls the snake
        `step_by_step`: Whether to run game step-by-step
        `episode_nb`: Current episode number
        `visual`: Whether to show game visualization "on"/"off"
        `debug`: Whether to show debug information
        `training`: Whether agent is in training mode
    """
    def __init__(self,
                 is_ai_control: bool,
                 step_by_step: bool,
                 episode_nb: int,
                 visual: str,
                 debug: bool,
                 training: bool
                 ) -> None:
        """Initialize game state with control settings."""
        self.is_ai_control = is_ai_control
        self.step_by_step = step_by_step
        self.episode_nb = episode_nb
        self.visual = True if visual == "on" else False

        self.gameover = False
        self.step = 0
        self.max_length = 0
        self.training = training
        self.debug = debug

        self.episode_lengths = []
        self.records = []
        self.total_episodes = 0
        self.moving_avg_window = 20
        self.start_time = datetime.now()

        if self.debug:
            self.print_initial_debug()

    def print_initial_debug(self) -> None:
        """Print initial debug informations."""
        print(f"{Col.YELLOW}{Col.BOLD}=== DEBUG MODE ==={Col.END}")
        initial_state = {
            "Visual": self.visual,
            "AI control": self.is_ai_control,
            "Step_by_step": self.step_by_step,
            "Training": self.training
        }
        for key, val in initial_state.items():
            status = Col.GREEN + 'ON' if val else Col.RED + 'OFF'
            print(f"{Col.CYAN}{Col.BOLD}{key}: {status}{Col.END}")

    def update(self, snake_len: int, epsilon: float) -> None:
        """Update state for new episode.

        Args:
            `snake_len`: Current snake length to update max length
            `epsilon`: Current e-greedy value of snake agent
        """
        self.total_episodes += 1
        self.episode_lengths.append(snake_len)
        self.agent_epsilon = epsilon

        if snake_len > self.max_length:
            self.max_length = snake_len
        self.records.append(self.max_length)
        
        self.step = 0
        self.gameover = False

    def print_periodic_stats(self, print_frequency: int) -> None:
        """Display periodic statistics about the snake performance."""
        avg_length = np.mean(self.episode_lengths[-100:])
        elapsed_time = datetime.now() - self.start_time

        print(f"\n=== Episode stats {self.total_episodes} ===")
        print(f"Time elapsed: {elapsed_time}")
        print(f"Mean Length ({print_frequency} last): {avg_length:.2f}")
        print(f"Length Record: {self.max_length}")
        print(f"Agent Epsilon: {self.agent_epsilon:.3f}")
        print("=====================================\n")

    def plot_statistics(self, save_path: str) -> None:
        """Generate and save visualization plots of game statistics."""
        if not save_path:
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # x-axis values for all episodes
        episodes = range(len(self.episode_lengths))
        
        # Plot raw episode lengths with some transparency
        ax1.plot(episodes, self.episode_lengths, label='Length per episode', alpha=0.3)

        # Add moving average if enough episodes have been recorded
        if len(self.episode_lengths) >= self.moving_avg_window:
            moving_avg = self.calculate_moving_average()
            # Plot starts from moving_avg_window-1 to align with corresponding episodes
            ax1.plot(episodes[self.moving_avg_window-1:],
                    moving_avg,
                    label=f'Moving mean ({self.moving_avg_window} episodes)',
                    linewidth=2)

        # first subplot appearance
        ax1.set_title('Snake length evolution')
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Length')
        ax1.legend()

        # Second subplot: Record evolution
        ax2.plot(episodes, self.records, label='Record evolution', color='red')
        ax2.set_title('Record evolution')
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Record')
        ax2.legend()

        plt.tight_layout()
        plt.savefig(f"save/{save_path}")
        plt.close()

    def calculate_moving_average(self) -> list:
        """Calculate the moving average of episode lengths."""
        return [np.mean(self.episode_lengths[i-self.moving_avg_window:i])
                for i in range(self.moving_avg_window, len(self.episode_lengths)+1)]


    def toggle_ai(self) -> None:
        """Toggle AI control mode and print debug info."""
        self.is_ai_control = not self.is_ai_control
        if self.debug:
            status = 'enabled' if self.is_ai_control else 'disabled'
            print(f"{Col.GREEN}AI control: {status}{Col.END}")

    def toggle_step_by_step(self) -> None:
        """Toggle step-by-step mode and print debug info."""
        self.step_by_step = not self.step_by_step
        if self.debug:
            status = 'enabled' if self.step_by_step else 'disabled'
            print(f"{Col.CYAN}Step-by-step: {status}{Col.END}")

    def should_step(self, step_move: str | None) -> bool:
        """Determine if game should advance a step.

        Args:
            `step_move`: Type of step requested ("step", "move", or None)

        Returns:
            `bool`: Whether game should advance:
                - True in normal mode
                - True if AI control and step_move is "step"
                - True if manual control and step_move is "move"
                - False otherwise in step-by-step mode
        """
        # Normal mode
        if not self.step_by_step:
            return True

        # AI step by step
        if self.is_ai_control and step_move == "step":
            return True

        # Player step by step
        if not self.is_ai_control and step_move == "move":
            return True

        # Step by step active + step_move == None
        return False
