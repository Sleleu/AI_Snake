import pygame as pg
from ..display.GameDraw import GameDraw
from ..agent.SnakeAgent import SnakeAgent
from .Spawner import Spawner
from ..agent.Interpreter import Interpreter
from .EventHandler import EventHandler
from .GameState import GameState
from ..display.Colors import Colors as Col
from ..display.display import print_experience
from settings import GRID_SIZE, FPS, GREEN_FRUITS_NB, \
                     RED_FRUITS_NB, SNAKE_SIZE, \
                     R_GREEN_FRUIT, R_RED_FRUIT, R_COLLISION


class SnakeGame:
    """Main game class handling snake logic and game loop."""
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
        self.gameState = GameState(is_ai_control,
                                   step_by_step,
                                   episode,
                                   visual,
                                   debug,
                                   train)
        self.interpreter = Interpreter()

        self.surface = surface
        if self.gameState.visual:
            self.clock = pg.time.Clock()

        if episode < 100:
            self.print_frequency = 10
        elif episode > 5000:
            self.print_frequency = max(episode // 200, 1)
        else:
            self.print_frequency = max(episode // 10, 1)

    def run(self) -> None:
        """Run multiple game episodes."""
        self.episode = 0
        for _ in range(self.gameState.episode_nb):
            is_continue = self.run_episode()
            if not is_continue:
                break

            self.episode += 1

            # Print statistics
            if self.episode % self.print_frequency == 0:
                self.gameState.print_periodic_stats(self.print_frequency)

            # Plot stats every 100 episodes
            if self.save and self.episode % 100 == 0:
                self.gameState.plot_statistics(self.save)

            # Autosave model
            if (self.episode in [10, 50, 100] or 
                self.episode % 500 == 0):
                path = f"model/{self.episode}_ep.pt"
                self.snakeAgent.save_model(path)
                print(f"Model autosave: {Col.GREEN}'{path}'{Col.END}")
        
        self.gameState.print_periodic_stats(self.episode)

    def episode_step(self, state: list) -> list:
        """Execute one step of an episode.

        Args:
            `state`: Current game state vector

        Returns:
            `list`: Next state vector after action
        """
        action = self.snakeAgent.get_action(state, self.gameState.debug)

        if self.gameState.is_ai_control:
            self.change_direction(action)
        self.move_snake()

        reward = self.reward()
        next_state = self.get_state()

        if self.gameState.debug:
            print_experience(state, action, reward, self.gameState.gameover)

        if self.gameState.training:
            self.snakeAgent.update(state,
                                   action,
                                   reward,
                                   next_state,
                                   self.gameState.gameover
                                   )
        self.gameState.step += 1
        return next_state

    def spawn_fruits(self) -> None:
        """Spawn initial green and red fruits."""
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

    def init_episode(self) -> None:
        """Initialize snake and direction for new episode."""
        self.actions = {"TOP": (-1, 0),
                        "BOTTOM": (1, 0),
                        "LEFT": (0, -1),
                        "RIGHT": (0, 1)}

        self.snake, self.direction = Spawner.snake_spawn(SNAKE_SIZE,
                                                         GRID_SIZE,
                                                         self.actions)
        fruits_nb = RED_FRUITS_NB + GREEN_FRUITS_NB
        if fruits_nb >= (GRID_SIZE**2 - len(self.snake)):
            raise AssertionError("Not enough place to spawn fruits")
        self.snake_head = self.snake[0]

    def run_episode(self) -> bool:
        """Run a single game episode.

        Returns:
            `bool`: False if game quit, True otherwise
        """
        self.init_episode()
        self.spawn_fruits()
        state = self.get_state()

        if self.gameState.visual:
            GameDraw.draw_game(
                surface=self.surface,
                gameState=self.gameState,
                snake=self.snake,
                green_fruits=self.green_fruits,
                red_fruits=self.red_fruits,
                episode=self.episode,
                snakeAgent=self.snakeAgent)
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
                GameDraw.draw_game(
                    surface=self.surface,
                    gameState=self.gameState,
                    snake=self.snake,
                    green_fruits=self.green_fruits,
                    red_fruits=self.red_fruits,
                    episode=self.episode,
                    snakeAgent=self.snakeAgent)
                self.clock.tick(FPS)

        self.gameState.update(len(self.snake),
                              self.snakeAgent.epsilon)

        return True

    def get_state(self) -> list:
        """Get current state from interpreter."""
        return self.interpreter.get_state(
            self.snake,
            self.green_fruits,
            self.red_fruits
        )

    def change_fruit_pos(self, fruit_lst: list[list]) -> None:
        """Update position of eaten fruit.

        Args:
            `fruit_lst`: List of fruits to update
        """
        fruit_lst.remove(self.snake_head)
        new_fruit = Spawner.fruit_spawn(self.snake, self.green_fruits,
                                        self.red_fruits, GRID_SIZE)
        if new_fruit is not None:
            fruit_lst.append(new_fruit)

    def reward(self) -> float:
        """Calculate reward for current step.

        Returns:
            `float`: Reward value based on game events
        """
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

    def move_snake(self) -> None:
        """Update snake position based on current direction."""
        new_head = [h + a for h, a in zip(self.snake_head,
                                          self.actions[self.direction])]
        self.snake.insert(0, new_head)
        self.snake_head = self.snake[0]

    def change_direction(self, key: int) -> None:
        """Change snake direction based on action.

        Args:
            `key`: Direction code (0:TOP, 1:BOTTOM, 2:LEFT, 3:RIGHT)
        """
        match key:
            case 0:
                self.direction = "TOP"
            case 1:
                self.direction = "BOTTOM"
            case 2:
                self.direction = "LEFT"
            case 3:
                self.direction = "RIGHT"
