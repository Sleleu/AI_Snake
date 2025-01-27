import pygame as pg
import numpy as np
from .Colors import Colors as Col
from settings import *


class SnakeGame:
    def __init__(self,
                 episode: int,
                 visual: str,
                 save: str | None,
                 model: str | None,
                 train: bool):

        self.episode_nb = episode
        self.visual = visual
        self.save = save
        self.model = model
        self.training = train

        self.init_game()

    def __str__(self):
        b = Col.GREEN + "=== Snake Attributes ===\n" + Col.END
        b += f"episode_nb: {self.episode_nb}\n"
        b += f"visual: {self.visual}\n"
        b += f"save: {self.save}\n"
        b += f"model: {self.model}\n"
        b += f"training: {self.training}\n"
        return b
    
    def init_game(self):
        pg.init()
        pg.display.set_caption('Learn2Slither')
        self.surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

    def run(self):
        for episode in range(self.episode_nb):
            print(f"episode: {episode}")
            self.start_new_game()

    def start_new_game(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE))
        self.snake_body = [[5, 5], [5, 4], [5, 3]]
        self.snake_head = self.snake_body[0]
        self.actions = {"UP": (-1, 0),
                        "DOWN": (1, 0),
                        "LEFT": (0, -1),
                        "RIGHT": (0, 1)}
        self.direction = "RIGHT"

        self.vision = {}

        self.place_items()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                if event.type == pg.KEYDOWN:
                    self.change_direction(event.key)
            self.draw_game()
            self.move_snake()

            self.clock.tick(FPS)

    def move_snake(self):
        new_head = [h + a for h, a in zip(self.snake_head, self.actions[self.direction])]
        self.snake_body.insert(0, new_head)
        self.snake_head = self.snake_body[0]
        self.snake_body.pop()

    def change_direction(self, key):
        match key:
            case pg.K_UP:
                self.direction = "UP"
            case pg.K_DOWN:
                self.direction = "DOWN"
            case pg.K_LEFT:
                self.direction = "LEFT"
            case pg.K_RIGHT:
                self.direction = "RIGHT"


    def place_items(self):
        self.grid.fill(0)
        for i, snake_part in enumerate(self.snake_body):
            self.grid[snake_part[0]][snake_part[1]] = 2 if i == 0 else 1

    def draw_game(self):
        self.surface.fill(Col.BG_COLOR)
        def draw_grid():
            for row in range(self.grid.shape[0]):
                for column in range(self.grid.shape[1]):
                    grid_cell = pg.Rect(column * CELL_SIZE + MARGIN,
                                        row * CELL_SIZE + MARGIN,
                                        CELL_SIZE,
                                        CELL_SIZE)
                    if (row + column) % 2 == 0:
                        pg.draw.rect(self.surface, Col.GRID_COLOR_EVEN, grid_cell)
                    else:
                        pg.draw.rect(self.surface, Col.GRID_COLOR_ODD, grid_cell)
        def draw_snake():
            for snake_part in self.snake_body:
                snake_cell = pg.Rect(snake_part[1] * CELL_SIZE + MARGIN,
                                     snake_part[0] * CELL_SIZE + MARGIN,
                                     CELL_SIZE,
                                     CELL_SIZE)
                if snake_part == self.snake_head:
                    pg.draw.rect(self.surface, Col.SNAKE_HEAD_COLOR, snake_cell)
                else:
                    pg.draw.rect(self.surface, Col.SNAKE_COLOR, snake_cell)

        draw_grid()
        draw_snake()
        pg.display.flip()