import os

from ba.element import Element
from ba.cv import Image

from . import image_handler

ImagesDir = os.path.join(os.path.dirname(__file__), "images")


class PageImage:
    name: str
    __source: Image
    elements: dict[str, Element] = {}

    def __init__(self, name: str) -> None:
        self.name = name
        with open(os.path.join(ImagesDir, name + ".png"), "rb") as f:
            self.__source = Image(f.read())

    def __getitem__(self, name: str):
        return self.elements[name]

    def addElement(self, name: str):
        func_prefix = self.name + "_" + name
        preprocess_func = getattr(image_handler, func_prefix + "_preprocess_func", None)
        like_func = getattr(image_handler, func_prefix + "_like_func", None)
        self.elements[name] = Element(
            Image(self.__source.src, preprocessFunc=preprocess_func), like_func
        )


"""主页面"""
home = PageImage("home")
"""开始游戏页面"""
start = PageImage("start")
start.addElement("icon")  # 右下角某个图标
"""沙勒新闻"""
notice = PageImage("notice")
notice.addElement("board")
