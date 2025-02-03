import pygame as pg
from .Colors import Colors as Col
from settings import CELL_SIZE, MARGIN, WIDTH, HEIGHT, MIN_AI_WIDTH, GRID_SIZE
from ..agent.Interpreter import Interpreter
from ..game.GameState import GameState
from ..agent.SnakeAgent import SnakeAgent
from .AIPanel import AIPanel


class GameDraw:
    """Handles all game drawing operations.

    Contains static methods to draw:
    - Game board and grid
    - Snake, fruits and game elements
    - Stats and status information
    - Neural network visualization via AIPanel
    """
    @staticmethod
    def draw_game(surface: pg.Surface,
                  gameState: GameState,
                  snake: list[list],
                  green_fruits: list[list],
                  red_fruits: list[list],
                  episode: int,
                  snakeAgent: SnakeAgent
                  ) -> None:
        """Draw complete game state.

        Args:
            `surface`: Pygame surface to draw on
            `gameState`: Current game state
            `snake`: Snake body coordinates [[y,x],...]
            `green_fruits`: Green fruit coordinates [[y,x],...]
            `red_fruits`: Red fruit coordinates [[y,x],...]
            `episode`: Current training episode number
            `snakeAgent`: Agent for getting action values
        """

        current_state = Interpreter.get_state(snake, green_fruits, red_fruits)
        current_action_values = snakeAgent.get_action_values(current_state)

        # Draw game features
        surface.fill(Col.BG_COLOR)
        GameDraw.draw_grid(surface)
        GameDraw.draw_snake(surface, snake)
        GameDraw.draw_fruits(surface, green_fruits, Col.GREEN_FRUIT_COLOR)
        GameDraw.draw_fruits(surface, red_fruits, Col.RED_FRUIT_COLOR)

        # Draw stats
        GameDraw.draw_length(surface, len(snake))
        GameDraw.draw_stat(surface,
                           "Episode",
                           episode,
                           10)
        GameDraw.draw_stat(surface,
                           "Max length",
                           gameState.max_length,
                           30)
        GameDraw.draw_stat(surface,
                           "Step",
                           gameState.step,
                           50)

        # Draw status
        GameDraw.draw_stat(surface,
                           "Training",
                           gameState.training,
                           HEIGHT - 20)
        GameDraw.draw_stat(surface,
                           "[A] AI",
                           gameState.is_ai_control,
                           HEIGHT - 40)
        GameDraw.draw_stat(surface,
                           "[P] Step-by-step",
                           gameState.step_by_step,
                           HEIGHT - 60)

        # Draw instructions
        if gameState.is_ai_control and gameState.step_by_step:
            GameDraw.draw_info(surface, "[SPACE] Next AI step")
        elif not gameState.is_ai_control:
            GameDraw.draw_info(surface, "Use ARROWS to move")

        # Draw neural network and state
        AIPanel.draw_neural_state(surface,
                                  current_state,
                                  gameState.is_ai_control)
        AIPanel.draw_neural_network(surface,
                                    current_state,
                                    current_action_values,
                                    gameState.is_ai_control)

        pg.display.flip()

    def draw_grid(surface: pg.Surface) -> None:
        """Draw checkered game grid.

        Args:
            `surface`: Pygame surface to draw on
        """
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                if (row + column) % 2:
                    color = Col.GRID_COLOR_EVEN
                else:
                    color = Col.GRID_COLOR_ODD
                pg.draw.rect(surface, color, pg.Rect(
                    column * CELL_SIZE + MARGIN,
                    row * CELL_SIZE + MARGIN,
                    CELL_SIZE, CELL_SIZE))

    def draw_snake(surface: pg.Surface, snake: list[list]) -> None:
        """Draw snake with different colored head.

        Args:
            `surface`: Pygame surface to draw on
            `snake`: Snake body coordinates [[y,x],...]
        """
        for i, part in enumerate(snake):
            color = Col.SNAKE_HEAD_COLOR if i == 0 else Col.SNAKE_COLOR
            pg.draw.rect(surface, color, pg.Rect(
                part[1] * CELL_SIZE + MARGIN,
                part[0] * CELL_SIZE + MARGIN,
                CELL_SIZE,
                CELL_SIZE))

    def draw_fruits(surface: pg.Surface,
                    fruits: list[list],
                    color: tuple
                    ) -> None:
        """Draw fruits with rounded rectangles.

        Args:
            `surface`: Pygame surface to draw on
            `fruits`: Fruit coordinates [[y,x],...]
            `color`: RGB color tuple for fruits
        """
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

    def draw_length(surface: pg.Surface, length: int) -> None:
        """Draw current snake length.

        Args:
            `surface`: Pygame surface to draw on
            `length`: Current snake length
        """
        font = pg.font.Font(None, 36)

        length_text = font.render(f"Length: {length}",
                                  True,
                                  Col.PG_CYAN)
        length_rect = length_text.get_rect(center=((WIDTH - MIN_AI_WIDTH) // 2,
                                                   MARGIN // 2))
        surface.blit(length_text, length_rect)

    def draw_info(surface: pg.Surface, info: str) -> None:
        """Draw game control information.

        Args:
            `surface`: Pygame surface to draw on
            `info`: Information text to display
        """
        font = pg.font.Font(None, 26)

        length_text = font.render(f"{info}",
                                  True,
                                  Col.PG_WHITE)
        length_rect = length_text.get_rect(
            center=((WIDTH - MIN_AI_WIDTH) // 2, MARGIN // 2),
            top=(HEIGHT - 40),
            )
        surface.blit(length_text, length_rect)

    def draw_stat(surface: pg.Surface,
                  key: str,
                  value: int | bool,
                  top: int
                  ) -> None:
        """Draw a game statistic or status.

        Args:
            `surface`: Pygame surface to draw on
            `key`: Stat name/key
            `value`: Value to display (bool or numeric)
            `top`: Vertical position
        """
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
