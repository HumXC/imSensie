from ba import images, scenes
from ba.element import Screen
from ..testing import TestDrives


def test():
    s = Screen(images.get("登录_通知"))
    e = scenes.登录_通知
    t = TestDrives(s)

    assert s.IsLike(e)
    t.Click(e.空白处)
    t.Show()
