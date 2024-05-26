from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("战术对抗赛"))
    e = scenes.战术对抗赛
    t = TestDrives(s)

    AssertScene(s, e)
    t.Click(e.每日奖励)
    t.Click(e.时间奖励)
    t.Show()
