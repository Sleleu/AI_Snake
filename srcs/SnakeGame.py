import pygame as pg

class SnakeGame:
    def __init__(self, episode: int, visual: str, save: str | None, train: bool):
        self.episode = episode
        self.visual = visual
        self.save = save
        self.training = train

    def __str__(self):
        b =  "=== Snake Attributes ===\n"
        b += f"episode: {self.episode}\n"
        b += f"visual: {self.visual}\n"
        b += f"save: {self.save}\n"
        b += f"training: {self.training}\n"
        return b
