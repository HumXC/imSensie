from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("获得奖励"))
    e = scenes.获得奖励
    t = TestDrives(s)

    assert s.IsLike(e)
    t.Click(e.空白处)
    t.Show()
