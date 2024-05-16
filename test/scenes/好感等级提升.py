from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("好感等级提升"))
    e = scenes.好感等级提升
    t = TestDrives(s)

    AssertScene(s, e)
    t.Click(e.空白处)
    t.Show()
