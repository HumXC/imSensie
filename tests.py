from ba import scenes
from ba.scenes import Edge
from test import scenes as tscenes


def testScenes():
    tscenes.登录_进入游戏.test()
    tscenes.登录_通知.test()
    tscenes.大厅.test()
    tscenes.大厅_全屏.test()
    tscenes.获得奖励.test()
    tscenes.好感等级提升.test()
