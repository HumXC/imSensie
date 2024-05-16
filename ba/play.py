import time
from typing import Callable
from ba.page_image import PageImage, attendance, main, notice, start

from cv2.typing import Size
from shiroko import Client, Importance
from shiroko.input import Input

from ba import page_image
from ba.element import Element
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


class Base:
    srk: Client
    input: Input
    pmg:PageImage
    
    def __init__(self, srk: Client,pmg:PageImage) -> None:
        self.srk = srk
        self.pmg=pmg
        self.input = self.srk.input
    def png(self):
        img = Image(self.srk.screencap.Png())
        if img.Size() != IMAGE_SIZE:
            raise ImageSizeMismatchError(IMAGE_SIZE, img.Size())
        return img

    def testPng(self) -> bool:
        try:
            self.png()
            return True
        except ImageSizeMismatchError:
            return False
class Start(Base):

    def __init__(self, srk: Client,pmg:PageImage ) -> None:
        super().__init__(srk,pmg)

    def Start(self, img: Image) ->  bool :
        if not page_image.start["icon"].IsLike(img):
            return False 
        point = (960, 540)
        self.input.Tap(point)
        return True 

class Attendance(Base):
    __main:"Main"
    def __init__(self, srk: Client, pmg: PageImage,main:"Main") -> None:
        super().__init__(srk, pmg)
        self.__main=main
    def Sign(self,img:Image)->bool:
        if not page_image.attendance["pen"].IsLike(img):
            return False

        self.input.Tap((800, 450))
        return True
        
        
class Main(Base):
    def __init__(self, srk: Client,pmg:PageImage) -> None:
        super().__init__(srk,pmg)

    def CloseNotice(self, img: Image):
        if not page_image.notice["board"].IsLike(img):
            return False
        if page_image.notice["checkbox"].IsLike(img):
            self.srk.input.Tap((1482, 926))
            time.sleep(0.1)
        # 关闭按钮
        self.srk.input.Tap((1660, 181))
        return True

    def Attendance(self, img: Image) -> bool:
        if not page_image.attendance["pen"].IsLike(img):
            return False

        self.input.Tap((800, 450))
        return True

    def Cofe(self):
        self.srk.input.Tap((193, 981))

    def Leson(self):
        self.srk.input.Tap((364, 991))

    def Crafting(self):
        self.srk.input.Tap((875, 981))

    def Shop(self):
        self.srk.input.Tap((1212, 991))

    def Campaign(self):
        self.srk.input.Tap((1740, 880))

    def Tasks(self):
        self.srk.input.Tap((150, 320))


class Player:
    start: Start
    main: Main
    srk: Client

    def __init__(self, srk: Client) -> None:
        self.main = Main(srk)
        self.start = Start(srk, self.main)
        self.srk = srk

    def png(self):
        img = Image(self.srk.screencap.Png())
        if img.Size() != IMAGE_SIZE:
            raise ImageSizeMismatchError(IMAGE_SIZE, img.Size())
        return img

    def testPng(self) -> bool:
        try:
            self.png()
            return True
        except ImageSizeMismatchError:
            return False

    def Play(self):
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

        while True:
            if self.testPng():
                break
            time.sleep(0.1)

        while True:
            try:
                img = self.png()
            except ImageSizeMismatchError:
                continue
            ok, main = self.start.Start(img)
            if not ok:
                continue
            main.Attendance(img):
                continue
            if self.main.CloseNotice(img):
                return
