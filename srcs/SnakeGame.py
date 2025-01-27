import pygame as pg
from .Colors import Colors as Col


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

    def __str__(self):
        b = Col.GREEN + "=== Snake Attributes ===\n" + Col.END
        b += f"episode_nb: {self.episode_nb}\n"
        b += f"visual: {self.visual}\n"
        b += f"save: {self.save}\n"
        b += f"model: {self.model}\n"
        b += f"training: {self.training}\n"
        return b
