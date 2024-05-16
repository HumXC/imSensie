import enum
from typing import Callable, Iterable, Protocol, cast

import cv2

from ba.cv import Image


class Preprocessor(Protocol):
    def Preprocessing(self, image: Image) -> Image: ...


class Likeable(Protocol):
    def Like(self, templ: Image) -> bool: ...


class Element(Preprocessor, Likeable): ...


class ActionType(enum.Enum):
    CLICK = "click"


class Action:
    type: ActionType


class ClickAction(Action, tuple[int, int]):
    def __new__(cls, x: int, y: int):
        return super().__new__(cls, (x, y))

    def __init__(self, x: int, y: int) -> None:
        self.type = ActionType.CLICK


class ElementClickAction(ClickAction, Element): ...


class Screen:
    src: Image

    def __init__(self, image: bytes | Image):
        if isinstance(image, Image):
            self.src = image
        else:
            self.src = Image(cast(bytes, image))

    def IsLike(self, likeable: Likeable) -> bool:
        return likeable.Like(self.src.Copy())
