from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("好感等级提升"))
    e = scenes.好感等级提升
    t = TestDrives(s)

    assert s.IsLike(e)
    t.Click(e.空白处)
    t.Show()
