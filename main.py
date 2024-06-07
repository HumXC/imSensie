from os import environ
import time
from dotenv import load_dotenv

load_dotenv()

import shiroko

import ba
from ba import scenes
from ba.game import Game
from ba.utils import *

ADDR: str = "192.168.1.17:15600"
ADDR: str = environ["SHIROKO_ADDR"]

srk = shiroko.Client(ADDR)
srk.window.ResetSize()
game = Game(srk)
game.Launch()


flags: dict[str, bool] = {}


def Goto(scene: scenes.Element) -> bool:
    ok, msg = game.Goto(scene)
    if not ok:
        print(msg)
        return False
    return True


def GetFlag(name: str) -> bool:
    if name not in flags:
        flags[name] = False
    return flags[name]


def SetFlag(name: str, value: bool):
    if name not in flags:
        flags[name] = False
    flags[name] = value


def 领取咖啡厅收益():
    ok = Goto(scenes.咖啡厅_收益)
    if not ok:
        return False
    game.DoAction(scenes.咖啡厅_收益.领取)


def 咖啡厅邀请(name: str) -> bool:
    ok = Goto(scenes.咖啡厅_MoomTalk)
    if not ok:
        return False
    latestStudents = []
    while True:
        ss = game.Find(scenes.咖啡厅_MoomTalk.邀请按钮)
        if latestStudents == ss:
            print(f"MoomTalo 邀请列表里没有找到 {name}")
            return False
        latestStudents = ss
        for s in ss:
            if s.name != name:
                continue
            ok, msg = game.DoAction(s)
            if not ok:
                print(msg)
                return False
            ok = game.Wait(scenes.咖啡厅_MoomTalk_通知, 3)
            if not ok:
                print("邀请失败")
                return False
            ok, msg = game.DoAction(scenes.咖啡厅_MoomTalk_通知.确认)
            if not ok:
                print(msg)
                return False


def 领取邮箱() -> bool:
    ok = game.Goto(scenes.邮箱)
    if not ok:
        return False
    return game.IfLikeAndDo(scenes.邮箱.一键领取)


def 领取工作任务奖励() -> bool:
    ok = game.Goto(scenes.工作任务)
    if not ok:
        return False
    return game.IfLikeAndDo(scenes.工作任务.一键领取)


def 领取战术对抗赛奖励():
    ok = Goto(scenes.战术对抗赛)
    if not ok:
        return False
    ok = game.IfLikeAndDo(scenes.战术对抗赛.每日奖励)
    if not ok:
        print("无法领取: 战术对抗赛.每日奖励")
    ok = Goto(scenes.战术对抗赛)
    if not ok:
        return False
    ok = game.IfLikeAndDo(scenes.战术对抗赛.时间奖励)
    if not ok:
        print("无法领取: 战术对抗赛.时间奖励")


def main():
    咖啡厅邀请("千世")
    领取战术对抗赛奖励()
    game.Goto(scenes.大厅)
    redPoints = game.FindRedPoint()
    for p in redPoints:
        print(str(p))
        if p == scenes.大厅.小组:
            game.Goto(scenes.小组大厅)
            continue
        if p == scenes.大厅.工作任务:
            领取工作任务奖励()
            continue
        if p == scenes.大厅.邮箱:
            领取邮箱()
            continue

    game.Goto(scenes.大厅_全屏)

    srk.window.ResetSize()
    print("Done")


if __name__ == "__main__":
    main()
