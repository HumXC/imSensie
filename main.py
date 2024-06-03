import time

import shiroko

import ba
from ba import scenes
from ba.game import Game
from ba.utils import *

ADDR: str = "192.168.1.17:15600"

srk = shiroko.Client(ADDR)
srk.window.ResetSize()
game = Game(srk)
game.Launch()


def 领取咖啡厅收益():
    game.Goto(scenes.咖啡厅_收益)
    game.DoAction(scenes.咖啡厅_收益.领取)


def 咖啡厅邀请(name: str) -> bool:
    while True:
        ok, msg = game.Goto(scenes.咖啡厅_MoomTalk_通知, findName=name)
        if ok:
            game.DoAction(scenes.咖啡厅_MoomTalk_通知.确认)
            return True
        print(msg)
        game.DoAction(scenes.咖啡厅_MoomTalk.上滑)


def main1():
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

    game.Goto(scenes.大厅_全屏)

    srk.window.ResetSize()
    print("Done")


def main():
    咖啡厅邀请("白子")
    srk.window.ResetSize()
    print("Done")


if __name__ == "__main__":
    main()
