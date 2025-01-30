import pygame as pg
import numpy as np
from .Colors import Colors as Col
from .GameDraw import GameDraw
from .SnakeAgent import SnakeAgent
from .Spawner import Spawner
from .display import print_state
from settings import GRID_SIZE, WIDTH, HEIGHT, FPS, \
                     GREEN_FRUITS_NB, RED_FRUITS_NB, SNAKE_SIZE


class SnakeGame:
    def __init__(self,
                 episode: int,
                 visual: str,
                 save: str | None,
                 model: str | None,
                 train: bool,
                 snake_size: int = SNAKE_SIZE,
                 green_fruits_nb: int = GREEN_FRUITS_NB,
                 red_fruits_nb: int = RED_FRUITS_NB,
                 grid_size: int = GRID_SIZE):

        self.episode_nb = episode
        self.visual = visual
        self.save = save
        self.model = model
        self.training = train
        self.max_length = 0
        self.snakeAgent = SnakeAgent(training=train, model=self.model)

        # Game settings
        self.snake_size = snake_size
        self.green_fruits_nb = green_fruits_nb
        self.red_fruits_nb = red_fruits_nb
        self.grid_size = grid_size

        if self.visual == "on":
            self.init_game()

    def init_game(self):
        pg.init()
        pg.display.set_caption('Learn2Slither')
        self.surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

    def run(self):
        self.episode = 0
        from .GameStats import GameStats
        self.gameStats = GameStats()
        for _ in range(self.episode_nb):
            self.start_new_game()
            self.save = "save"
            self.gameStats.get_stats(self)
            self.episode += 1

    def start_new_game(self):
        self.actions = {"TOP": (-1, 0),
                        "BOTTOM": (1, 0),
                        "LEFT": (0, -1),
                        "RIGHT": (0, 1)}
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE))
        try:
            self.snake, self.direction = Spawner.snake_spawn(self.snake_size,
                                                             self.grid_size,
                                                             self.actions)
            fruits_nb = self.red_fruits_nb + self.green_fruits_nb
            assert fruits_nb <= (self.grid_size**2 - len(self.snake)), \
                "Not enough place to spawn fruits"
        except AssertionError as e:
            print(f"{Col.RED}{Col.BOLD}{e.__class__.__name__}: {e}{Col.END}")
            if self.visual == "on":
                pg.quit()
            exit(1)
        self.snake_head = self.snake[0]
        self.gameover = False
        self.step = 0

        self.green_fruits = []
        self.red_fruits = []
        for _ in range(self.green_fruits_nb):
            self.green_fruits.append(Spawner.fruit_spawn(self.snake,
                                                         self.green_fruits,
                                                         self.red_fruits,
                                                         self.grid_size))
        for _ in range(self.red_fruits_nb):
            self.red_fruits.append(Spawner.fruit_spawn(self.snake,
                                                       self.green_fruits,
                                                       self.red_fruits,
                                                       self.grid_size))

        self.place_items()
        self.snakeAgent.state = self.get_state()
        if self.visual == "on":
            self.draw_game()
            self.clock.tick(FPS)
        while True:
            if self.visual == "on":
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit(0)
                    if event.type == pg.KEYDOWN:
                        self.change_direction(event.key)
                        if event.key == pg.K_s:
                            self.snakeAgent.save_model("manual_save.pkl")

            action = self.snakeAgent.select_action()

            self.change_direction(action)
            self.move_snake()
            self.snakeAgent.reward = self.reward()
            self.snakeAgent.next_state = self.get_state()
            self.snakeAgent.update_policy()
            self.snakeAgent.state = self.snakeAgent.next_state
            if self.gameover:
                break
            self.step += 1
            if self.visual == "on":
                self.draw_game()
                self.clock.tick(FPS)

        if len(self.snake) > self.max_length:
            self.max_length = len(self.snake)
        if self.snakeAgent.reward == 1000:  # win test
            if self.visual == "on":
                self.draw_game()
            print("WON")
            pg.time.delay(1000)

    def get_item_dist(self, obj_lst):
        head_y, head_x = self.snake_head
        results = []
        directions = {
            'top': ([y for y, x in obj_lst if x == head_x and y < head_y],
                    lambda y: head_y - y),
            'bottom': ([y for y, x in obj_lst if x == head_x and y > head_y],
                       lambda y: y - head_y),
            'left': ([x for y, x in obj_lst if y == head_y and x < head_x],
                     lambda x: head_x - x),
            'right': ([x for y, x in obj_lst if y == head_y and x > head_x],
                      lambda x: x - head_x)}

        for objs, dist_func in directions.values():
            mask = 1 if objs else 0
            dist = min(map(dist_func, objs)) / GRID_SIZE if objs else 0
            results.extend([mask, dist])
        return results


    def get_state(self) -> list:
        state = []
        head_y, head_x = self.snake_head
        dist_wall = [head_y / GRID_SIZE,                    # top
                     (GRID_SIZE - head_y - 1) / GRID_SIZE,  # bottom
                     head_x / GRID_SIZE,                    # left
                     (GRID_SIZE - head_x - 1) / GRID_SIZE]  # right
        green_fruits_dists = self.get_item_dist(self.green_fruits)
        red_fruits_dists = self.get_item_dist(self.red_fruits)
        body_dists = self.get_item_dist(self.snake[1:])
        for i in range(4):
            state.append(dist_wall[i])
            state.append(green_fruits_dists[i * 2])
            state.append(green_fruits_dists[i * 2 + 1])
            state.append(red_fruits_dists[i * 2])
            state.append(red_fruits_dists[i * 2 + 1])
            state.append(body_dists[i * 2])
            state.append(body_dists[i * 2 + 1])
        #print_state(state)
        return state

    def reward(self) -> float:

        def change_fruit_pos(fruit_lst):
            fruit_lst.remove(self.snake_head)
            new_fruit = Spawner.fruit_spawn(self.snake, self.green_fruits,
                                            self.red_fruits, self.grid_size)
            if new_fruit is not None:
                fruit_lst.append(new_fruit)
        if self.snake_head in self.snake[1:]:
            self.gameover = True
            return -20
        elif GRID_SIZE in self.snake_head or -1 in self.snake_head:
            self.gameover = True
            return -20
        elif self.snake_head in self.green_fruits:
            change_fruit_pos(self.green_fruits)
            if len(self.snake) >= (self.grid_size**2 - (self.red_fruits_nb)):
                self.gameover = True
                return 100
            return 20
        elif self.snake_head in self.red_fruits:
            self.snake.pop()
            self.snake.pop()
            change_fruit_pos(self.red_fruits)
            if len(self.snake) <= 0:
                self.gameover = True
                return -20
            return -5
        else:
            self.snake.pop()
            return -0.5

    def move_snake(self):
        new_head = [h + a for h, a in zip(self.snake_head,
                                          self.actions[self.direction])]
        self.snake.insert(0, new_head)
        self.snake_head = self.snake[0]

    def change_direction(self, key):
        match key:
            case pg.K_UP:
                self.direction = "TOP"
            case pg.K_DOWN:
                self.direction = "BOTTOM"
            case pg.K_LEFT:
                self.direction = "LEFT"
            case pg.K_RIGHT:
                self.direction = "RIGHT"

    def place_items(self):
        self.grid.fill(0)
        for i, snake_part in enumerate(self.snake):
            self.grid[snake_part[0]][snake_part[1]] = 2 if i == 0 else 1

    def draw_game(self):
        self.surface.fill(Col.BG_COLOR)
        GameDraw.draw_grid(self.surface, self.grid)
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
