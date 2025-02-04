from srcs.game.SnakeGame import SnakeGame
from srcs.display.Colors import Colors as Col
from settings import WIDTH, HEIGHT
import pygame as pg
import argparse


class ArgError(Exception):
    pass


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--episode",
                        type=int, default=10,
                        help="Number of episodes to run.")
    parser.add_argument("-v", "--visual",
                        type=str, choices=("on", "off"), default="on",
                        help="Enable or disable game GUI. Default 'on'.")
    parser.add_argument("-plot",
                        type=str, default=None,
                        help="Filename to save statistics plots.")
    parser.add_argument("-m", "--model",
                        type=str, default=None,
                        help="Path to a pre-trained model to load.")
    parser.add_argument("-t", "--train",
                        action="store_true",
                        help="Enable training mode.")
    parser.add_argument("-step-by-step", action="store_true",
                        help="Enable step-by-step mode.")
    parser.add_argument("-p", "--player", action="store_true",
                        help="Enable player mode.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug mode.")

    return parser.parse_args()


def init_pygame():
    pg.init()
    return pg.display.set_mode((WIDTH, HEIGHT))


def main():
    args = None
    try:
        args = parse_arguments()

        surface = None
        if args.visual == "off" and args.step_by_step:
            raise ArgError("Can't off visual and play in step-by-step")
        if args.visual == "off" and args.player:
            raise ArgError("Can't off visual and use player commands")
        if args.visual == "on":
            surface = init_pygame()
            pg.display.set_caption('Learn2Slither')
        game = SnakeGame(episode=args.episode,
                         visual=args.visual,
                         plot=args.plot,
                         model=args.model,
                         train=args.train,
                         step_by_step=args.step_by_step,
                         is_ai_control=not args.player,
                         debug=args.debug,
                         surface=surface)
        game.run()
    except AssertionError as e:
        print(f"{Col.RED}{Col.BOLD}{e.__class__.__name__}: {e}{Col.END}")
        exit(1)
    except Exception as e:
        print(f"{Col.RED}{Col.BOLD}{e.__class__.__name__}: {e}{Col.END}")
        exit(1)
    finally:
        if args is not None and args.visual == "on":
            pg.quit()


if __name__ == "__main__":
    main()
