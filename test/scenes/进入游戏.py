from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("进入游戏"))
    e = scenes.进入游戏
    t = TestDrives(s)

    assert s.IsLike(e)
    t.Click(e.空白处)
    t.Show()
