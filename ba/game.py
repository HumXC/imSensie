import time

from cv2.typing import Size
from shiroko import Client, Importance
from shiroko.input import Input

from ba import scenes
from ba import element
from ba.element import Clickable
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


def WhichScenes(s: element.Screen) -> element.Scenes:
    for e in scenes.All:
        if s.IsLike(e):
            return e
    return scenes.Unknow


class Game:
    srk: Client
    input: Input

    def __init__(self, srk: Client) -> None:
        self.srk = srk
        self.input = self.srk.input

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

    def Click(self, p: Clickable):
        self.input.Tap((p[0], p[1]))

    def Run(self):
        def click(p: Clickable):
            def f():
                self.Click(p)

            return f

        actions = {
            scenes.进入游戏: click(scenes.进入游戏.空白处),
            scenes.大厅: click(scenes.大厅.小组),
            scenes.小组大厅: click(scenes.小组大厅.返回),
            scenes.小组大厅_签到奖励: click(scenes.小组大厅_签到奖励.空白处),
            scenes.可以点击空白处: click(scenes.可以点击空白处.空白处),
        }
        done = False
        while True:
            if done:
                break
            s = WhichScenes(self.Screen())
            for k, v in actions.items():
                if s == k:
                    if s == scenes.小组大厅:
                        done = True
                    v()
                    break
