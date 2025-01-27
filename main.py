from srcs.SnakeGame import SnakeGame
from srcs.Parser import Parser

def main():
    parser = Parser()
    game = SnakeGame(episode=parser.args.episode,
                     visual=parser.args.visual,
                     save=parser.args.save,
                     model=parser.args.model,
                     train=parser.args.train)
    print(game)

if __name__ == "__main__":
    main()