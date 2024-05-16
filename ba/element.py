from typing import Callable, Protocol, cast

import cv2

from ba.cv import Image


class Element(Protocol):
    def Preprocessing(self, image: Image) -> Image: ...


class Likeable(Protocol):
    def Like(self, templ: Image) -> bool: ...


Clickable = tuple[int, int]
Swipable = tuple[Clickable, Clickable]
Action = Clickable | Swipable


class Scenes(Element, Likeable, Protocol): ...


class Screen:
    src: Image

    def __init__(self, image: bytes | Image):
        if isinstance(image, Image):
            self.src = image
        else:
            self.src = Image(cast(bytes, image))

    def IsLike(self, likeable: Likeable) -> bool:
        return likeable.Like(self.src.Copy())
