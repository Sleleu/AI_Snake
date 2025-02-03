from ..display.Colors import Colors as Col


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
        if self.debug:
            print(f"{Col.YELLOW}{Col.BOLD}=== DEBUG MODE ==={Col.END}")
            initial_state = {
                "Visual": self.visual,
                "AI control": self.is_ai_control,
                "Step_by_step": self.step_by_step,
                "Training": self.training
                }
            for key, val in initial_state.items():
                status = Col.GREEN + 'ON' if val else Col.RED + 'OFF'
                print(f"{Col.CYAN}{Col.BOLD}{key}: ", end='')
                print(f"{status}{Col.END}")

    def update(self, snake_len: int) -> None:
        """Update state for new episode.

        Args:
            `snake_len`: Current snake length to update max length
        """
        if snake_len > self.max_length:
            self.max_length = snake_len
        self.step = 0
        self.gameover = False

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
