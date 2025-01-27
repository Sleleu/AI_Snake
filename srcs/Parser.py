import argparse


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-e", "--episode",
                                 type=int, default=10)
        self.parser.add_argument("-v", "--visual",
                                 type=str, choices=("on", "off"), default="on")
        self.parser.add_argument("-s", "--save",
                                 type=str, default=None)
        self.parser.add_argument("-m", "--model",
                                 type=str, default=None)
        self.parser.add_argument("-train", action="store_true")
        self.args = self.parser.parse_args()
