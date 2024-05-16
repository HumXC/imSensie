import time

import shiroko

import ba
from ba.game import Game
from ba.utils import *

ADDR: str = "192.168.1.17:15600"


def main():
    srk = shiroko.Client(ADDR)
    game = Game(srk)
    game.Launch()
    game.Run()
    srk.window.ResetSize()
    print("Done")


if __name__ == "__main__":
    main()
