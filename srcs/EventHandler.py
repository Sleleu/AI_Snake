import pygame as pg

class EventHandler:

    @staticmethod
    def handle_event(event, gameState, snakeAgent, change_direction):
        if event.type == pg.QUIT:
            return True, None
        
        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_s:
                    snakeAgent.save_model("manual_save.pt")
                    print("Model saved as 'manual_save.pt'")
                case pg.K_p:
                    snakeAgent.epsilon += 0.05
                    print(snakeAgent.epsilon)
                case pg.K_m:
                    snakeAgent.epsilon -= 0.05
                    print(snakeAgent.epsilon)
                case pg.K_a:
                    gameState.toggle_ai()
                case pg.K_t:
                    gameState.toggle_step_by_step()
                case pg.K_SPACE:
                    return False, "step"
                case pg.K_UP | pg.K_DOWN | pg.K_LEFT | pg.K_RIGHT if not gameState.is_ai_control:
                    direction = {
                        pg.K_UP: 0, pg.K_DOWN: 1,
                        pg.K_LEFT: 2, pg.K_RIGHT: 3
                    }[event.key]
                    change_direction(direction)
                    return False, "move"
        
        return False, None

    @staticmethod
    def handle(gameState, snakeAgent, change_direction):
        if not gameState.visual:
            return False, None

        action = None
        for event in pg.event.get():
            quit_game, new_action = EventHandler.handle_event(
                event, gameState, snakeAgent, change_direction)
            if quit_game:
                return True, None
            if new_action:
                action = new_action
        
        return False, action
