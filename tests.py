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
    tscenes.咖啡厅.test()
    tscenes.咖啡厅_收益.test()
    tscenes.咖啡厅_说明.test()
    tscenes.工作任务.test()
    tscenes.小组大厅.test()
    tscenes.小组大厅_签到奖励.test()
    tscenes.登录_更新提醒.test()


# testScenes()
# tscenes.咖啡厅_收益.test()
tscenes.登录_更新提醒.test()
