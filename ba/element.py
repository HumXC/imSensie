from typing import Callable, Protocol, cast

import cv2

from ba.cv import Image


class Element(Protocol):
    def Preprocessing(self, image: Image) -> Image: ...


class Likeable(Protocol):
    def Like(self, templ: Image) -> bool: ...


Point = cv2.typing.Point


class Scenes(Element, Likeable, Protocol): ...


class Screen:
    src: Image

    def __init__(self, image: bytes | Image):
        if type(image) is Image:
            self.src = image
        else:
            self.src = Image(cast(bytes, image))

    def IsLike(self, likeable: Likeable) -> bool:
        """判断是否相似，输入的图像将被自动应用 self.src.preprocssFunc"""
        return likeable.Like(self.src.Copy())


class Elemendt:
    img: Image
    """
    IsLike 调用的函数，输入是 原图 和 被比较图
    返回是否相似
    """
    likeFunc: Callable[[Image, Image], bool] | None

    def __init__(
        self,
        img: Image,
        likeFunc: Callable[[Image, Image], bool] | None = None,
    ):
        self.img = img
        self.likeFunc = likeFunc

    def IsLike(self, templ: Image) -> bool:
        """判断是否相似，输入的图像将被自动应用 self.img.preprocssFunc"""
        if self.img is None:
            raise Exception("Image is None")
        t = templ.Copy()
        self.img.precessFunc(t)
        if self.likeFunc is None:
            raise Exception("No likeFunc")
        return self.likeFunc(self.img.Copy(), t)
