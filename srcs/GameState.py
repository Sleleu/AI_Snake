class GameState:
    def __init__(self, is_ai_control, step_by_step, episode_nb, visual):
        self.is_ai_control = is_ai_control
        self.step_by_step = step_by_step
        self.episode_nb = episode_nb
        self.visual = True if visual == "on" else False

        self.gameover = False
        self.step = 0
        self.max_length = 0
        
        self.debug = False # TODO make debug option with print

    def update(self, snake_len):
        if snake_len > self.max_length:
            self.max_length = snake_len
        self.step = 0
        self.gameover = False
    
    def toggle_ai(self):
        self.is_ai_control = not self.is_ai_control
        if self.debug:
            print(f"AI control: {'enabled' if self.is_ai_control else 'disabled'}")
    def toggle_step_by_step(self):
        self.step_by_step = not self.step_by_step
        if self.debug:
            print(f"Step-by-step: {'enabled' if self.step_by_step else 'disabled'}")

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
