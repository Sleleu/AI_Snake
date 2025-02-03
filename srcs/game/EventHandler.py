import pygame as pg
from ..agent.SnakeAgent import SnakeAgent
from .GameState import GameState
from typing import Callable


class EventHandler:
    """Handles game events and user input.

    Contains static methods to handle:
    - Key presses for game control
    - AI/manual control toggling
    - Model saving
    - Movement in manual mode
    """
    @staticmethod
    def handle_event(event: pg.event.Event,
                     gameState: GameState,
                     snakeAgent: SnakeAgent,
                     change_direction: Callable[[int], None]
                     ) -> tuple[bool, str | None]:
        if event.type == pg.QUIT:
            return True, None
        move_keys = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)
        if event.type == pg.KEYDOWN:
            match event.key:
                case pg.K_s:
                    if gameState.training:
                        snakeAgent.save_model("model/manual_save.pt")
                        print("Model saved as 'model/manual_save.pt'")
                    else:
                        print("Save model in training not allowed")
                case pg.K_a:
                    gameState.toggle_ai()
                case pg.K_p:
                    gameState.toggle_step_by_step()
                case pg.K_SPACE:
                    return False, "step"
                case event.key if event.key in move_keys:
                    if not gameState.is_ai_control:
                        direction = {
                            pg.K_UP: 0, pg.K_DOWN: 1,
                            pg.K_LEFT: 2, pg.K_RIGHT: 3
                        }[event.key]
                        change_direction(direction)
                    return False, "move"

        return (False, None)

    @staticmethod
    def handle(gameState: GameState,
               snakeAgent: SnakeAgent,
               change_direction: Callable[[int], None]
               ) -> tuple[bool, str | None]:
        """Process all pending pygame events.

        Args:
            `gameState`: Current game state
            `snakeAgent`: Agent for model saving
            `change_direction`: Callback to update snake direction

        Returns:
            `tuple[bool, str]`: (quit_game, action) where:
                - quit_game indicates if game should exit
                - action is the last processed action or None
        """
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

        return (False, action)
