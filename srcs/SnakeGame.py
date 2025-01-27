import pygame as pg
import numpy as np
import random
from .Colors import Colors as Col
from .GameDraw import GameDraw
from settings import GRID_SIZE, WIDTH, HEIGHT, FPS, \
                     GREEN_FRUITS_NB, RED_FRUITS_NB


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
        self.gameover = False

        self.green_fruits = []
        self.red_fruits = []
        for _ in range(GREEN_FRUITS_NB):
            self.green_fruits.append(self.add_fruit())
        for _ in range(RED_FRUITS_NB):
            self.red_fruits.append(self.add_fruit())

        self.vision = {}

        self.place_items()
        while True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)
                if event.type == pg.KEYDOWN:
                    self.change_direction(event.key)
            self.draw_game()
            self.move_snake()
            reward = self.reward()
            if self.gameover:
                break

    def reward(self) -> float:

        def change_fruit_pos(fruit_lst):
            fruit_lst.remove(self.snake_head)
            new_fruit = self.add_fruit()
            if new_fruit is not None:
                fruit_lst.append(new_fruit)

        if self.snake_head in self.snake_body[1:]:
            self.gameover = True
            return -100
        elif GRID_SIZE in self.snake_head or -1 in self.snake_head:
            self.gameover = True
            return -100
        elif self.snake_head in self.green_fruits:
            change_fruit_pos(self.green_fruits)
            self.snake_body.insert(0, self.snake_head)
            return 10
        elif self.snake_head in self.red_fruits:
            change_fruit_pos(self.red_fruits)
            self.snake_body.pop()
            if len(self.snake_body) <= 0:
                self.gameover = True
                return -100
            return -10
        else:
            return -0.2

    def move_snake(self):
        new_head = [h + a for h, a in zip(self.snake_head,
                                          self.actions[self.direction])]
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

    def add_fruit(self):
        while True:
            occupied = self.snake_body + self.green_fruits + self.red_fruits
            fruit = [random.randrange(0, GRID_SIZE),
                     random.randrange(0, GRID_SIZE)]
            if fruit not in occupied:
                return fruit
            if not np.any(self.grid == 0):
                return None

    def draw_game(self):
        self.surface.fill(Col.BG_COLOR)
        GameDraw.draw_grid(self.surface, self.grid)
        GameDraw.draw_snake(self.surface, self.snake_body)
        GameDraw.draw_fruits(self.surface, self.green_fruits,
                             Col.GREEN_FRUIT_COLOR)
        GameDraw.draw_fruits(self.surface, self.red_fruits,
                             Col.RED_FRUIT_COLOR)
        pg.display.flip()
