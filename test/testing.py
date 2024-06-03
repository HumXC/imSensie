from os import path
from typing import Any
import cv2
import numpy
from ba import images
from ba.element import (
    ClickAction,
    ElementClickAction,
    Findable,
    Ocrable,
    Screen,
    SlideAction,
)
from ba.scenes import All, Element
from PIL import Image, ImageDraw, ImageFont

IsShowImage = False
FontName = path.join(path.join(path.dirname(__file__), "../blob/MiSans-Normal.ttf"))
font = ImageFont.truetype(FontName, size=32)


class TestDrives:
    screen: Screen

    def __init__(self, s: Screen):
        self.screen = s
        self.img = s.src.ToPillowImage()
        self.draw = ImageDraw.Draw(self.img)

    def Test(self, field: Any):
        if isinstance(field, type):
            return
        if isinstance(field, ElementClickAction):  # 检查字段是否为字符串类型
            self.ElementClick(field)
        elif isinstance(field, ClickAction):  # 检查字段是否为字符串类型
            self.Click(field)
        elif isinstance(field, SlideAction):
            self.Slide(field)
        elif hasattr(field, "__orig_bases__"):
            for b in field.__orig_bases__:
                if b.__name__ == Ocrable.__name__:
                    self.Ocr(field)
                elif b.__name__ == Findable.__name__:
                    self.Find(field)

    def Show(self):
        self.screen.src.src = numpy.array(self.img)
        self.screen.src.CvtColor(cv2.COLOR_RGB2BGR).Apply()
        if not IsShowImage:
            return
        self.screen.src.Show()[0]()

    def Click(self, c: ClickAction):
        self.draw.ellipse(
            [(c[0] - 5, c[1] - 5), (c[0] + 5, c[1] + 5)], fill=(255, 0, 0)
        )
        self.draw.text(c, f"{c.name} (sleep {c.sleep}s)", font=font, fill=(0, 0, 255))

    def ElementClick(self, c: ElementClickAction):
        for rect in c.area:
            p1 = (rect[0], rect[1])
            p2 = (rect[0] + rect[2], rect[1] + rect[3])
            self.draw.rectangle([p1, p2], outline=(255, 0, 0), width=2)
        self.Click(c)

    def Ocr(self, o: Ocrable):
        rect = o.area
        p1 = (rect[0], rect[1])
        p2 = (rect[0] + rect[2], rect[1] + rect[3])
        self.draw.rectangle([p1, p2], outline=(255, 0, 0), width=2)
        self.draw.text(p1, o.name, font=font, fill=(0, 0, 255))

        result = str(o.Ocr(self.screen.src))
        self.draw.text(p2, result, font=font, fill=(0, 0, 255))

    def Find(self, f: Findable):
        result: tuple[Any] = f.Find(self.screen.src)
        for r in result:
            self.Test(r)

    def Slide(self, s: SlideAction):
        self.draw.line([s.start, s.end], fill=(255, 0, 0), width=2)
        self.draw.text(
            s.start, f"{s.name} (duration {s.duration}ms)", font=font, fill=(0, 0, 255)
        )


def AssertScene(s: Screen, e: Element):
    for i in All:
        if i == e:
            assert s.IsLike(i)
            continue
        assert not s.IsLike(i)
