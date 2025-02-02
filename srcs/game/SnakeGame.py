import pygame as pg
from ..display.Colors import Colors as Col
from .GameDraw import GameDraw
from ..agent.SnakeAgent import SnakeAgent
from .Spawner import Spawner
from ..agent.Interpreter import Interpreter
from .EventHandler import EventHandler
from .GameState import GameState
from ..display.display import print_state, print_experience
from settings import GRID_SIZE, FPS, GREEN_FRUITS_NB, \
                     RED_FRUITS_NB, SNAKE_SIZE, \
                     R_GREEN_FRUIT, R_RED_FRUIT, R_COLLISION, HEIGHT


class SnakeGame:
    def __init__(self,
                 episode: int,
                 visual: str,
                 save: str | None,
                 model: str | None,
                 train: bool,
                 step_by_step: bool,
                 is_ai_control: bool,
                 debug: bool,
                 surface=None):

        self.save = save
        self.model = model
        self.snakeAgent = SnakeAgent(training=train, model=self.model)
        self.gameState = GameState(
            is_ai_control,
            step_by_step,
            episode,
            visual,
            debug,
            train)
        self.interpreter = Interpreter()

        self.surface = surface
        if self.gameState.visual:
            self.clock = pg.time.Clock()

    def run(self):
        self.episode = 0
        from ..display.GameStats import GameStats
        self.gameStats = GameStats()
        for _ in range(self.gameState.episode_nb):
            is_continue = self.run_episode()
            if not is_continue:
                break
            self.save = "save"
            self.gameStats.get_stats(self)
            self.episode += 1
            if (self.episode == 10
                or self.episode == 50
                or self.episode == 100):
                self.snakeAgent.save_model(f"model/{self.episode}_ep.pt")
            if self.episode % 400 == 0:
                self.snakeAgent.save_model(f"model/{self.episode}_ep.pt")

    def episode_step(self, state):
        action = self.snakeAgent.get_action(state, self.gameState.debug)
        
        if self.gameState.is_ai_control:
            self.change_direction(action)
        self.move_snake()
        
        reward = self.reward()
        next_state = self.get_state()
        
        if self.gameState.debug:
            print_experience(state, action, reward, self.gameState.gameover)
        
        if self.gameState.training:
            self.snakeAgent.update(state, action, reward, next_state, self.gameState.gameover)
            self.snakeAgent.learn()
        self.gameState.step += 1
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

    def run_episode(self):
        self.init_episode()
        self.spawn_fruits()
        state = self.get_state()

        if self.gameState.visual:
            self.draw_game()
            self.clock.tick(FPS)
        
        while not self.gameState.gameover:
            quit_game, step_move = EventHandler.handle(
                self.gameState,
                self.snakeAgent,
                self.change_direction, 
            )
            if quit_game:
                return False

            if self.gameState.should_step(step_move):
                state = self.episode_step(state)

            if self.gameState.visual:
                self.draw_game()
                self.clock.tick(FPS)
        
        self.gameState.update(len(self.snake))
            
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
        reward, self.gameState.gameover = self.interpreter.get_reward(
            self.snake_head,
            self.snake,
            self.green_fruits,
            self.red_fruits
        )
        if reward == R_GREEN_FRUIT:
            self.change_fruit_pos(self.green_fruits)
            if len(self.snake) >= (GRID_SIZE**2 - (RED_FRUITS_NB)):
                self.gameState.gameover = True
                return 100
        elif reward == R_RED_FRUIT:
            self.snake.pop()
            if len(self.snake) <= 1:
                self.gameState.gameover = True
                return R_COLLISION
            self.snake.pop()
            self.change_fruit_pos(self.red_fruits)
        else:
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
        GameDraw.draw_stat(self.surface, "Episode", self.episode, 10)
        GameDraw.draw_stat(self.surface, "Max length", self.gameState.max_length, 30)
        GameDraw.draw_stat(self.surface, "Step", self.gameState.step, 50)

        GameDraw.draw_stat(self.surface, "Training", self.gameState.training, HEIGHT - 20)
        GameDraw.draw_stat(self.surface, "[A] AI", self.gameState.is_ai_control, HEIGHT - 40)
        GameDraw.draw_stat(self.surface, "[P] Step-by-step", self.gameState.step_by_step, HEIGHT - 60)

        if self.gameState.is_ai_control and self.gameState.step_by_step:
            GameDraw.draw_info(self.surface, "[SPACE] Next AI step")
        elif not self.gameState.is_ai_control:
            GameDraw.draw_info(self.surface, "Use ARROWS to move")

        pg.display.flip()
