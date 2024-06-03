import enum
from os import name
from typing import Protocol, TypeVar, cast

from ba.cv import Image

T = TypeVar("T", covariant=True)


class Preprocessor(Protocol):
    def Preprocessing(self, image: Image) -> Image: ...


class Likeable(Protocol):
    def Like(self, templ: Image) -> bool: ...


class Ocrable[T](Protocol):
    area: tuple[int, int, int, int]  # 用于描述识别的区域，debug用
    name: str

    def Ocr(self, image: Image) -> T: ...


class Findable[T](Protocol):
    def Find(self, templ: Image) -> tuple[T]: ...


class Element(Preprocessor, Likeable, Protocol):
    area: list[tuple[int, int, int, int]]  # 用于描述识别的区域，debug用
    name: str

    def __str__(self) -> str:
        return self.name


class ActionType(enum.Enum):
    CLICK = "click"
    ELEMENT_CLIEK = "element_click"
    FINDABLE_CLICK = "findable_click"
    SLIDE = "slide"


class Action:
    type: ActionType
    name: str = "Unknown"
    sleep: int = 0  # seconds

    def __init__(self, sleep: int | None = None) -> None:
        if sleep is not None:
            self.sleep = sleep  # seconds

    def __str__(self) -> str:
        return self.name


class ClickAction(Action, tuple[int, int]):
    type = ActionType.CLICK

    def __new__(cls, name: str, x: int, y: int, sleep: int | None = None):
        s = super().__new__(cls, (x, y))
        s.name = name
        return s

    def __init__(self, name: str, x: int, y: int, sleep: int | None = None):
        super().__init__(sleep)


class FindableClickAction(Action, Findable[ClickAction]):
    type = ActionType.FINDABLE_CLICK

    def __init__(self, name: str, sleep: int | None = None) -> None:
        self.name = name
        super().__init__(sleep)


class ElementClickAction(ClickAction, Element):
    type: ActionType = ActionType.ELEMENT_CLIEK


class SlideAction(Action):
    type = ActionType.SLIDE
    start: tuple[int, int]
    end: tuple[int, int]
    duration: int

    def __init__(
        self, name: str, start: tuple[int, int], end: tuple[int, int], duration: int
    ) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration


# ElementActions = ElementClickAction | OtherElementAction
ElementActions = ElementClickAction


class Screen:
    src: Image

    def __init__(self, image: bytes | Image):
        if isinstance(image, Image):
            self.src = image
        else:
            self.src = Image(cast(bytes, image))

    def IsLike(self, likeable: Likeable) -> bool:
        return likeable.Like(self.src.Copy())
