import pygame as pg


class Colors:
    # Game colors from : https://www.color-hex.com/color-palette/61235
    BG_COLOR = pg.Color((9, 24, 51))
    GRID_COLOR_EVEN = pg.Color((10, 189, 198))
    GRID_COLOR_ODD = pg.Color((9, 179, 188))
    SNAKE_COLOR = pg.Color(((234, 0, 217)))
    SNAKE_HEAD_COLOR = pg.Color((113, 28, 145))
    GREEN_FRUIT_COLOR = pg.Color((0, 255, 0))
    RED_FRUIT_COLOR = pg.Color((255, 0, 0))
    TEXT_COLOR = pg.Color('white')
    TEXT_RED = pg.Color('red')
    TEXT_GREEN = pg.Color('green')
    TEXT_CYAN = pg.Color('cyan')

    # ASCII colors
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
