from ..display.Colors import Colors as Col

class GameState:
    def __init__(self, is_ai_control, step_by_step, episode_nb, visual, debug, training):
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
                print(f"{Col.CYAN}{Col.BOLD}{key}: ", end='')
                print(f"{Col.GREEN + 'ON' if val else Col.RED + 'OFF'}{Col.END}")

    def update(self, snake_len):
        if snake_len > self.max_length:
            self.max_length = snake_len
        self.step = 0
        self.gameover = False
    
    def toggle_ai(self):
        self.is_ai_control = not self.is_ai_control
        if self.debug:
            print(f"{Col.GREEN}AI control: {'enabled' if self.is_ai_control else 'disabled'}{Col.END}")

    def toggle_step_by_step(self):
        self.step_by_step = not self.step_by_step
        if self.debug:
            print(f"{Col.CYAN}Step-by-step: {'enabled' if self.step_by_step else 'disabled'}{Col.END}")

    def should_step(self, step_move: str | None) -> bool:
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
