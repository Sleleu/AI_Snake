import pygame as pg
from .Colors import Colors as Col
from settings import CELL_SIZE, MARGIN, WIDTH, HEIGHT, MIN_AI_WIDTH, GRID_SIZE
from ..agent.Interpreter import Interpreter
from ..game.GameState import GameState
from ..agent.SnakeAgent import SnakeAgent
from .AIPanel import AIPanel


class GameDraw:

    @staticmethod
    def draw_game(
        surface: pg.Surface,
        gameState: GameState,
        snake: list,
        green_fruits: list,
        red_fruits: list,
        episode: int,
        snakeAgent: SnakeAgent
        ):

        current_state = Interpreter.get_state(snake, green_fruits, red_fruits)
        current_action_values = snakeAgent.get_action_values(current_state)

        # Draw game features
        surface.fill(Col.BG_COLOR)
        GameDraw.draw_grid(surface, GRID_SIZE)
        GameDraw.draw_snake(surface, snake)
        GameDraw.draw_fruits(surface, green_fruits, Col.GREEN_FRUIT_COLOR)
        GameDraw.draw_fruits(surface, red_fruits, Col.RED_FRUIT_COLOR)
        
        # Draw stats
        GameDraw.draw_length(surface, len(snake))
        GameDraw.draw_stat(surface, "Episode", episode, 10)
        GameDraw.draw_stat(surface, "Max length", gameState.max_length, 30)
        GameDraw.draw_stat(surface, "Step", gameState.step, 50)

        # Draw status
        GameDraw.draw_stat(surface, "Training", gameState.training, HEIGHT - 20)
        GameDraw.draw_stat(surface, "[A] AI", gameState.is_ai_control, HEIGHT - 40)
        GameDraw.draw_stat(surface, "[P] Step-by-step", gameState.step_by_step, HEIGHT - 60)

        # Draw instructions
        if gameState.is_ai_control and gameState.step_by_step:
            GameDraw.draw_info(surface, "[SPACE] Next AI step")
        elif not gameState.is_ai_control:
            GameDraw.draw_info(surface, "Use ARROWS to move")

        # Draw neural network and state
        AIPanel.draw_neural_state(surface, current_state, gameState.is_ai_control)
        AIPanel.draw_neural_network(surface, current_state, current_action_values, gameState.is_ai_control)

        pg.display.flip()

    def draw_grid(surface, grid_size):
        for row in range(grid_size):
            for column in range(grid_size):
                if (row + column) % 2:
                    color = Col.GRID_COLOR_EVEN
                else:
                    color = Col.GRID_COLOR_ODD
                pg.draw.rect(surface, color, pg.Rect(
                    column * CELL_SIZE + MARGIN,
                    row * CELL_SIZE + MARGIN,
                    CELL_SIZE, CELL_SIZE))

    def draw_snake(surface, snake):
        for i, part in enumerate(snake):
            color = Col.SNAKE_HEAD_COLOR if i == 0 else Col.SNAKE_COLOR
            pg.draw.rect(surface, color, pg.Rect(
                part[1] * CELL_SIZE + MARGIN,
                part[0] * CELL_SIZE + MARGIN,
                CELL_SIZE,
                CELL_SIZE))

    def draw_fruits(surface, fruits, color):
        for fruit in fruits:
            pg.draw.rect(
                surface,
                color,
                pg.Rect(
                    fruit[1] * CELL_SIZE + MARGIN,
                    fruit[0] * CELL_SIZE + MARGIN,
                    CELL_SIZE,
                    CELL_SIZE),
                border_radius=50,
                border_top_left_radius=10)

    def draw_length(surface, length):
        font = pg.font.Font(None, 36)

        length_text = font.render(f"Length: {length}",
                                  True,
                                  Col.PG_CYAN)
        length_rect = length_text.get_rect(center=((WIDTH - MIN_AI_WIDTH) // 2, MARGIN // 2))
        surface.blit(length_text, length_rect)

    def draw_info(surface, info):
        font = pg.font.Font(None, 26)

        length_text = font.render(f"{info}",
                                  True,
                                  Col.PG_WHITE)
        length_rect = length_text.get_rect(
            center=((WIDTH - MIN_AI_WIDTH) // 2, MARGIN // 2),
            top=(HEIGHT - 40),
            )
        surface.blit(length_text, length_rect)

    def draw_stat(surface, key, value, top):
        font = pg.font.Font(None, 24)

        key_text = font.render(f"{key}: ", True, Col.PG_WHITE)
        
        if isinstance(value, bool):
            status_text = "ON" if value else "OFF"
            status_color = Col.PG_GREEN if value else Col.PG_RED
        else:
            status_text = str(value)
            status_color = Col.PG_CYAN
        value_text = font.render(status_text, True, status_color)
    
        key_rect = key_text.get_rect(top=top, left=5)
        value_rect = value_text.get_rect(top=top, left=key_rect.right)
        surface.blit(key_text, key_rect)
        surface.blit(value_text, value_rect)
