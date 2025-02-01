import pygame as pg
import numpy as np
from .Colors import Colors as Col
from .GameDraw import GameDraw
from .SnakeAgent import SnakeAgent
from .Spawner import Spawner
from .Interpreter import Interpreter
from .EventHandler import EventHandler
from .display import print_state
from settings import GRID_SIZE, FPS, GREEN_FRUITS_NB, \
                     RED_FRUITS_NB, SNAKE_SIZE, \
                     R_GREEN_FRUIT, R_RED_FRUIT

class SnakeGame:
    def __init__(self,
                 episode: int,
                 visual: str,
                 save: str | None,
                 model: str | None,
                 train: bool,
                 surface=None):

        self.episode_nb = episode
        self.visual = visual
        self.save = save
        self.model = model
        self.training = train
        self.max_length = 0
        self.snakeAgent = SnakeAgent(training=train, model=self.model)
        self.interpreter = Interpreter()

        self.surface = surface
        if self.visual == "on":
            self.clock = pg.time.Clock()

    def run(self):
        self.episode = 0
        from .GameStats import GameStats
        self.gameStats = GameStats()
        for _ in range(self.episode_nb):
            is_continue = self.run_episode()
            if not is_continue:
                break
            self.save = "save"
            self.gameStats.get_stats(self)
            self.episode += 1  

    def episode_step(self, state):
        action = self.snakeAgent.get_action(state)
        
        self.change_direction(action)
        self.move_snake()
        
        reward = self.reward()
        next_state = self.get_state()
        
        if self.training:
            self.snakeAgent.update(state, action, reward, next_state, self.gameover)
            self.snakeAgent.learn()
        self.step += 1
        return next_state

    def spawn_fruits(self):
        self.green_fruits = []
        self.red_fruits = []
        for _ in range(GREEN_FRUITS_NB):
            self.green_fruits.append(
                Spawner.fruit_spawn(self.snake, self.green_fruits,
                                    self.red_fruits, GRID_SIZE))
        for _ in range(RED_FRUITS_NB):
            self.red_fruits.append(
                Spawner.fruit_spawn(self.snake, self.green_fruits,
                                    self.red_fruits, GRID_SIZE))   

    def init_episode(self):
        self.actions = {"TOP": (-1, 0), "BOTTOM": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
        
        self.snake, self.direction = Spawner.snake_spawn(SNAKE_SIZE, GRID_SIZE, self.actions)
        fruits_nb = RED_FRUITS_NB + GREEN_FRUITS_NB
        if fruits_nb >= (GRID_SIZE**2 - len(self.snake)):
            raise AssertionError("Not enough place to spawn fruits")
        self.snake_head = self.snake[0]
        self.gameover = False
        self.step = 0

    def run_episode(self):
        self.init_episode()
        self.spawn_fruits()
        state = self.get_state()

        if self.visual == "on":
            self.draw_game()
            self.clock.tick(FPS)
        
        while not self.gameover:
            if EventHandler.handle(self.visual, self.snakeAgent, self.change_direction):
                return False
            
            state = self.episode_step(state)
            if self.visual == "on":
                self.draw_game()
                self.clock.tick(FPS)
        if len(self.snake) > self.max_length:
            self.max_length = len(self.snake)
            
        return True
    
    def get_state(self) -> list:
        return self.interpreter.get_state(
            self.snake_head,
            self.snake,
            self.green_fruits,
            self.red_fruits
        )

    def change_fruit_pos(self, fruit_lst):
        fruit_lst.remove(self.snake_head)
        new_fruit = Spawner.fruit_spawn(self.snake, self.green_fruits,
                                        self.red_fruits, GRID_SIZE)
        if new_fruit is not None:
            fruit_lst.append(new_fruit)

    def reward(self) -> float:
        reward, self.gameover = self.interpreter.get_reward(
            self.snake_head,
            self.snake,
            self.green_fruits,
            self.red_fruits
        )
        if reward == R_GREEN_FRUIT:
            self.change_fruit_pos(self.green_fruits)
            if len(self.snake) >= (GRID_SIZE**2 - (RED_FRUITS_NB)):
                self.gameover = True
                return 100
        elif reward == R_RED_FRUIT:
            self.snake.pop()
            self.snake.pop()
            self.change_fruit_pos(self.red_fruits)
        elif reward == 0:
            self.snake.pop()
        return reward

    def move_snake(self):
        new_head = [h + a for h, a in zip(self.snake_head,
                                          self.actions[self.direction])]
        self.snake.insert(0, new_head)
        self.snake_head = self.snake[0]

    def change_direction(self, key):
        match key:
            case 0:
                self.direction = "TOP"
            case 1:
                self.direction = "BOTTOM"
            case 2:
                self.direction = "LEFT"
            case 3:
                self.direction = "RIGHT"

    def draw_game(self):
        self.surface.fill(Col.BG_COLOR)
        GameDraw.draw_grid(self.surface, GRID_SIZE)
        GameDraw.draw_snake(self.surface, self.snake)
        GameDraw.draw_fruits(self.surface, self.green_fruits,
                             Col.GREEN_FRUIT_COLOR)
        GameDraw.draw_fruits(self.surface, self.red_fruits,
                             Col.RED_FRUIT_COLOR)
        GameDraw.draw_length(self.surface, len(self.snake))
        GameDraw.draw_value(self.surface, "episode", self.episode, 10)
        GameDraw.draw_value(self.surface, "max length", self.max_length, 30)
        GameDraw.draw_value(self.surface, "step", self.step, 50)
        pg.display.flip()
