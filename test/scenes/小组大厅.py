from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("小组大厅"))
    e = scenes.小组大厅
    t = TestDrives(s)

    assert s.IsLike(e)

    t.Click(e.返回)
    t.Show()
