from srcs.SnakeGame import SnakeGame
from srcs.Parser import Parser
from srcs.Colors import Colors as Col
from settings import WIDTH, HEIGHT
import pygame as pg


def init_pygame():
    pg.init()
    return pg.display.set_mode((WIDTH, HEIGHT))

def main():
    try:
        parser = Parser()

        surface = None
        if parser.args.visual == "on":
            surface = init_pygame()
            pg.display.set_caption('Learn2Slither')

        game = SnakeGame(episode=parser.args.episode,
                        visual=parser.args.visual,
                        save=parser.args.save,
                        model=parser.args.model,
                        train=parser.args.train,
                        surface=surface)
        game.run()
    except AssertionError as e:
        print(f"{Col.RED}{Col.BOLD}{e.__class__.__name__}: {e}{Col.END}")
        exit(1)
    except Exception as e:
        print(f"{Col.RED}{Col.BOLD}{e.__class__.__name__}: {e}{Col.END}")
        exit(1)
    finally:
        if parser.args.visual == "on":
            pg.quit()


if __name__ == "__main__":
    main()
