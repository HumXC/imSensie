from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("大厅_全屏"))
    e = scenes.大厅_全屏
    t = TestDrives(s)

    AssertScene(s, e)

    t.Click(e.退出全屏)
    t.Show()
