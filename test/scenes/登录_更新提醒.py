from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("登录_更新提醒"))
    e = scenes.登录_更新提醒
    t = TestDrives(s)

    AssertScene(s, e)

    t.Click(e.确认)
    t.Show()
