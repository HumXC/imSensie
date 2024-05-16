from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("工作任务"))
    e = scenes.工作任务
    t = TestDrives(s)

    assert s.IsLike(e)
    assert s.IsLike(e.一键领取)
    assert s.IsLike(e.领取)

    t.Click(e.一键领取)
    t.Click(e.领取)
    t.Show()
