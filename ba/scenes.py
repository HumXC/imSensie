from ba import images
from ba.cv import Image
from ba.element import Point, Scenes


class scenes(Scenes):
    src: Image

    def __init__(self, image: Image) -> None:
        self.src = self.Preprocessing(image.Copy())

    def Preprocessing(self, image: Image) -> Image: ...

    def Like(self, templ: Image) -> bool: ...


class __进入游戏(scenes):
    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("进入游戏").Copy())

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((96, 994, 125, 68))

    def Like(self, templ: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)

    def Start(self) -> Point:
        return (1, 1)


进入游戏 = __进入游戏()
