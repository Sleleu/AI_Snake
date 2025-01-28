import pygame as pg
from .Colors import Colors as Col
from settings import CELL_SIZE, MARGIN, WIDTH


class GameDraw:

    @staticmethod
    def draw_grid(surface, grid):
        for row in range(grid.shape[0]):
            for column in range(grid.shape[1]):
                grid_cell = pg.Rect(column * CELL_SIZE + MARGIN,
                                    row * CELL_SIZE + MARGIN,
                                    CELL_SIZE,
                                    CELL_SIZE)
                if (row + column) % 2 == 0:
                    pg.draw.rect(surface=surface,
                                 color=Col.GRID_COLOR_EVEN,
                                 rect=grid_cell)
                else:
                    pg.draw.rect(surface=surface,
                                 color=Col.GRID_COLOR_ODD,
                                 rect=grid_cell)

    @staticmethod
    def draw_snake(surface, snake_body):
        snake_head = snake_body[0]
        for snake_part in snake_body:
            snake_cell = pg.Rect(snake_part[1] * CELL_SIZE + MARGIN,
                                 snake_part[0] * CELL_SIZE + MARGIN,
                                 CELL_SIZE,
                                 CELL_SIZE)

            if snake_part == snake_head:
                pg.draw.rect(surface=surface,
                             color=Col.SNAKE_HEAD_COLOR,
                             rect=snake_cell)
            else:
                pg.draw.rect(surface=surface,
                             color=Col.SNAKE_COLOR,
                             rect=snake_cell)

    @staticmethod
    def draw_fruits(surface, fruits_lst, color):
        for fruit in fruits_lst:
            fruit_cell = pg.Rect(fruit[1] * CELL_SIZE + MARGIN,
                                 fruit[0] * CELL_SIZE + MARGIN,
                                 CELL_SIZE,
                                 CELL_SIZE)
            pg.draw.rect(surface=surface,
                         color=color,
                         rect=fruit_cell,
                         border_radius=50,
                         border_top_left_radius=10)
    
    @staticmethod
    def draw_length(surface, length):
        font = pg.font.Font(None, 36)

        length_text = font.render(f"length: {length}", True, Col.GRID_COLOR_EVEN)
        length_rect = length_text.get_rect(center=(WIDTH // 2, MARGIN // 2))
        surface.blit(length_text, length_rect)

    @staticmethod
    def draw_value(surface, key, value, top):
        font = pg.font.Font(None, 26)

        length_text = font.render(f"{key}: {value}", True, Col.TEXT_COLOR)
        length_rect = length_text.get_rect(topleft=(10, top))
        surface.blit(length_text, length_rect)
