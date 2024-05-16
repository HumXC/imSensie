from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("大厅_全屏"))
    e = scenes.大厅_全屏
    t = TestDrives(s)

    assert s.IsLike(e)
    t.Click(e.退出全屏)
    t.Show()
