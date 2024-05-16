from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("咖啡厅"))
    e = scenes.咖啡厅
    t = TestDrives(s)

    assert s.IsLike(e)
    assert s.IsLike(e.收益)
    assert s.IsLike(e.邀请劵)
    t.Click(e.收益)
    t.Click(e.邀请劵)
    t.Show()
