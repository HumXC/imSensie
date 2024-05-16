from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("咖啡厅_说明"))
    e = scenes.咖啡厅_说明
    t = TestDrives(s)

    AssertScene(s, e)
    t.Click(e.空白处)
    t.Show()
