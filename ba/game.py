import time
from typing import cast

from cv2.typing import Size
from shiroko import Client, Importance
from shiroko.input import Input

from ba import scenes
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
        time.sleep(0.2)
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
