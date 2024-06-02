import enum
from typing import Generic, Protocol, TypeVar, cast

from ba.cv import Image

T = TypeVar("T", covariant=True)


class Preprocessor(Protocol):
    def Preprocessing(self, image: Image) -> Image: ...


class Likeable(Protocol):
    def Like(self, templ: Image) -> bool: ...


class Ocrable(Protocol[T]):
    def Ocr(self, image: Image) -> T: ...


class Findable(Protocol[T]):
    def Find(self, templ: Image) -> tuple[T]: ...


class Element(Preprocessor, Likeable, Protocol): ...


class ActionType(enum.Enum):
    CLICK = "click"
    ELEMENT_CLIEK = "element_click"
    FINDABLE_CLICK = "findable_click"


class Action:
    type: ActionType
    name: str = "Unknown"

    def __str__(self) -> str:
        return self.name


class ClickAction(Action, tuple[int, int]):
    type = ActionType.CLICK

    def __new__(cls, name: str, x: int, y: int):
        s = super().__new__(cls, (x, y))
        s.name = name
        return s


class FindableClickAction(Action, Findable[ClickAction]):
    type = ActionType.FINDABLE_CLICK

    def __init__(self, name: str) -> None:
        self.name = name


class ElementClickAction(ClickAction, Element):
    type: ActionType = ActionType.ELEMENT_CLIEK


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
