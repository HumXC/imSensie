from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("大厅"))
    e = scenes.大厅
    t = TestDrives(s)

    AssertScene(s, e)

    t.Click(e.工作任务)
    t.Click(e.邮箱)
    t.Click(e.全屏大厅)
    t.Click(e.咖啡厅)
    t.Click(e.日程)
    t.Click(e.成员)
    t.Click(e.小组)
    t.Click(e.商店)
    t.Click(e.业务区)
    t.Show()
