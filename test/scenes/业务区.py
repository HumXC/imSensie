from ba import images, scenes
from ba.element import Screen
from ..testing import AssertScene, TestDrives


def test():
    s = Screen(images.get("业务区"))
    e = scenes.业务区
    t = TestDrives(s)

    AssertScene(s, e)
    t.Click(e.任务)
    t.Click(e.故事)
    t.Click(e.悬赏通缉)
    t.Click(e.特别委托)
    t.Click(e.学院交流会)
    t.Click(e.总力战)
    t.Click(e.战术综合测试)
    t.Click(e.战术对抗赛)
    t.Show()
