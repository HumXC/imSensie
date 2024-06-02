from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("咖啡厅_MoomTalk"))
    e = scenes.咖啡厅_MoomTalk
    t = TestDrives(s)

    AssertScene(s, e)
    t.Show()
