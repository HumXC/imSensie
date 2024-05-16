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
        return element.Screen(self.Png())

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

    def __doAction(self, a: scenes.Action):
        if a.type == element.ActionType.CLICK:
            self.Click(cast(element.ClickAction, a))

    def __goto(
        self, frome: scenes.Scenes, to: scenes.Scenes, actions: list[scenes.Action]
    ) -> bool:
        while True:
            c = self.CurrentScene()
            if c == to:
                return True
            if c == frome:
                for a in actions:
                    self.__doAction(a)
                continue
            if c == scenes.Unknow:
                self.Click(scenes.Unknow.空白处)
                time.sleep(1)
                continue
            else:
                return False

    def Goto(self, s: scenes.Scenes) -> bool:
        while True:
            cs = self.CurrentScene()
            if cs == scenes.Unknow:
                self.Click(scenes.Unknow.空白处)
                time.sleep(1)
                cs = self.CurrentScene()
                continue
            if cs == scenes.登录_更新提醒:
                cs = self.CurrentScene()
                self.Click(scenes.登录_更新提醒.确认)
                time.sleep(1)
                continue

            path = self.grap.FindPath(cs, s)
            if path is None:
                raise Exception("no path")
            actions = self.grap.FindActions(path)
            for i in range(len(path)):
                if not self.__goto(cs, path[i], actions[i]):
                    return False
                cs = self.CurrentScene()
            return True
