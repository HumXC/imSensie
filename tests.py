from typing import Any
import cv2
from ba import game, images, scenes
from ba.element import Screen
from ba.scenes import Edge, Graph
from test import scenes as tscenes, testing

testing.IsShowImage = False


def testScenes():
    tscenes.登录_进入游戏.test()
    tscenes.登录_通知.test()
    tscenes.大厅.test()
    tscenes.大厅_全屏.test()
    tscenes.获得奖励.test()
    tscenes.好感等级提升.test()
    tscenes.咖啡厅.test()
    tscenes.咖啡厅_收益.test()
    tscenes.咖啡厅_说明.test()
    tscenes.工作任务.test()
    tscenes.小组大厅.test()
    tscenes.小组大厅_签到奖励.test()
    tscenes.登录_更新提醒.test()
    tscenes.邮箱.test()
    tscenes.战术对抗赛.test()
    tscenes.业务区.test()
    tscenes.咖啡厅_MoomTalk.test()
    tscenes.咖啡厅_MoomTalk_通知.test()


# testScenes()
# Graph().Draw("MiSans", "graph.png")
