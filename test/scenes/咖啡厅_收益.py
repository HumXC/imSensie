from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("咖啡厅_收益"))
    e = scenes.咖啡厅_收益
    t = TestDrives(s)

    AssertScene(s, e)
    assert s.IsLike(e.领取)
    t.Click(e.领取)
    t.Click(e.空白处)
    t.Show()
