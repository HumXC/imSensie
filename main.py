import time

import shiroko

import ba
from ba import scenes
from ba.game import Game
from ba.utils import *

ADDR: str = "192.168.1.17:15600"


def main():
    srk = shiroko.Client(ADDR)
    srk.window.ResetSize()
    game = Game(srk)
    game.Launch()
    game.Goto(scenes.大厅)
    redPoints = game.FindRedPoint()
    for p in redPoints:
        print(str(p))
        if p == scenes.大厅.小组:
            game.Goto(scenes.小组大厅)
            continue
        if p == scenes.大厅.工作任务:
            game.Goto(scenes.工作任务)
            game.IfLikeAndDo(scenes.工作任务.一键领取)
            continue
        if p == scenes.大厅.邮箱:
            game.Goto(scenes.邮箱)
            game.IfLikeAndDo(scenes.邮箱.一键领取)
            continue
        if p == scenes.大厅.业务区:
            game.Goto(scenes.业务区)
            redPoints = game.FindRedPoint()
            for p in redPoints:
                print(str(p))
                if p == scenes.业务区.战术对抗赛:
                    game.Goto(scenes.战术对抗赛)
                    game.IfLikeAndDo(scenes.战术对抗赛.每日奖励)
                    time.sleep(1)
                    game.Goto(scenes.战术对抗赛)
                    game.IfLikeAndDo(scenes.战术对抗赛.时间奖励)
            continue
    game.Goto(scenes.咖啡厅_收益)
    game.IfLikeAndDo(scenes.咖啡厅_收益.领取)

    game.Goto(scenes.大厅_全屏)

    srk.window.ResetSize()
    print("Done")


if __name__ == "__main__":
    main()
