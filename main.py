import time

import shiroko

import ba
from ba import scenes
from ba.game import Game
from ba.utils import *

ADDR: str = "192.168.1.17:15600"


def main():
    srk = shiroko.Client(ADDR)
    game = Game(srk)
    game.Launch()

    game.Goto(scenes.工作任务)
    if game.Screen().IsLike(scenes.工作任务.一键领取):
        game.Click(scenes.工作任务.一键领取)
    srk.window.ResetSize()
    print("Done")


if __name__ == "__main__":
    main()
