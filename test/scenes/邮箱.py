from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("邮箱"))
    e = scenes.邮箱
    t = TestDrives(s)

    AssertScene(s, e)

    t.Click(e.返回)
    t.Click(e.一键领取)
    t.Show()
