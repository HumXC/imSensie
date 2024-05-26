import time
from typing import Callable, cast

from cv2.typing import Size
from shiroko import Client, Importance
from shiroko.input import Input

from ba import scenes, utils
from ba import element
from ba.element import ClickAction
from ba.cv import Image


class ImageSizeMismatchError(Exception):
    """Raised when the image size does not match the screen size."""

    target: Size
    got: Size

    def __init__(self, target: Size, got: Size) -> None:
        self.target = target
        self.got = got


Pkgname = "com.RoamingStar.BlueArchive"
Activity = "com.yostar.supersdk.activity.YoStarSplashActivity"
SCREEN_SIZE = (1080, 1920)
IMAGE_SIZE = (1920, 1080)

RedPoints = [
    [scenes.大厅.工作任务, (191, 327, 48, 56)],
    [scenes.大厅.小组, (371, 983, 59, 60)],
    [scenes.大厅.业务区, (1778, 767, 71, 76)],
    [scenes.大厅.邮箱, (1686, 3, 48, 57)],
    [scenes.业务区.战术对抗赛, (1712, 559, 43, 46)],
    [scenes.业务区.总力战, (1458, 562, 48, 46)],
]
YellowPoints = [
    [scenes.大厅.咖啡厅, (216, 981, 62, 65)],
    [scenes.业务区.总力战, (1458, 562, 48, 46)],
    [scenes.业务区.悬赏通缉, (1205, 557, 48, 56)],
    [scenes.业务区.学院交流会, (1160, 792, 53, 49)],
]


class Game:
    srk: Client
    input: Input
    grap: scenes.Graph
    lastScreen: element.Screen

    def __init__(self, srk: Client) -> None:
        self.srk = srk
        self.input = self.srk.input
        self.grap = scenes.Graph()

    def Png(self):
        img = Image(self.srk.screencap.Png())
        if img.Size() != IMAGE_SIZE:
            raise ImageSizeMismatchError(IMAGE_SIZE, img.Size())
        return img

    def Screen(self) -> element.Screen:
        self.lastScreen = element.Screen(self.Png())
        return self.lastScreen

    def IfLikeAndDo(self, a: element.ElementActions) -> bool:
        isLike = self.Screen().IsLike(a)
        if isLike:
            self.DoAction(a)
        return isLike

    def Launch(self):
        self.srk.window.SetSize(SCREEN_SIZE[0], SCREEN_SIZE[1])
        # 唤醒屏幕
        self.srk.input.Wakeup()
        # 启动
        self.srk.shell.StartApp(Pkgname + "/" + Activity)
        while True:
            i = self.srk.shell.GetAppImportance(Pkgname)
            if i == Importance.FOREGROUND:
                if Image(self.srk.screencap.Png()).Size() == IMAGE_SIZE:
                    break
            time.sleep(0.1)

    def Kill(self):
        self.srk.shell.StopApp(Pkgname)

    def Click(self, p: ClickAction):
        self.input.Tap(p)

    def CurrentScene(self):
        s = self.Screen()
        for e in scenes.All:
            if s.IsLike(e):
                return e
        return scenes.Unknow

    def DoAction(self, a: scenes.Action) -> bool:
        result = False
        if a.type == element.ActionType.CLICK:
            result = True
            self.Click(cast(element.ClickAction, a))
        elif a.type == element.ActionType.ELEMENT_CLIEK:
            a = cast(element.ElementClickAction, a)
            isLike = self.lastScreen.IsLike(a)
            result = isLike
            if isLike:
                self.Click(a)
        time.sleep(0.5)
        return result

    def Special(self, cs: element.Element) -> bool:
        if cs == scenes.Unknow:
            self.Click(scenes.Unknow.空白处)
            time.sleep(1)
            return True
        if cs == scenes.登录_更新提醒:
            cs = self.CurrentScene()
            self.Click(scenes.登录_更新提醒.确认)
            time.sleep(1)
            return True
        if cs == scenes.获得奖励:
            print("获得奖励")
            self.Click(scenes.获得奖励.继续)
            return True
        return False

    def Goto(self, s: element.Element) -> bool:
        while True:
            cs = self.CurrentScene()
            if cs == s:
                time.sleep(0.5)
                return True
            if self.Special(cs):
                continue
            path = self.grap.FindPath(cs, s)
            if path is None:
                raise Exception("no path")
            action = self.grap.FindActions(path[:2])[0]
            for a in action:
                if not self.DoAction(a):
                    return False

    def __findPoint(
        self,
        function: Callable[[Image, Callable[[int, int], bool]], list[tuple[int, int]]],
    ) -> list[element.Element]:
        s = self.Screen()
        result = []
        pts = function(s.src, lambda x, y: True)
        for p in pts:
            for rp in RedPoints:
                px1, py1 = rp[1][0], rp[1][1]
                px2, py2 = px1 + rp[1][2], py1 + rp[1][3]
                if px1 <= p[0] <= px2 and py1 <= p[1] <= py2:
                    result.append(rp[0])
                    continue
        return result

    def FindRedPoint(self) -> list[element.Element]:
        return self.__findPoint(utils.FindRedPoint)

    def FindYellowPoint(self) -> list[element.Element]:
        return self.__findPoint(utils.FindYellowPoint)
