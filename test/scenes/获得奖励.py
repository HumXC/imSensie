from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("获得奖励"))
    e = scenes.获得奖励
    t = TestDrives(s)

    AssertScene(s, e)
    t.Click(e.空白处)
    t.Show()
