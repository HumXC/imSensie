from typing import Iterable, cast
from ba import images
from ba.cv import Image
from ba.element import Action, ClickAction, ClickableElement, Element


class Scenes(Element):
    src: Image

    def __init__(self, image: Image) -> None:
        self.src = self.Preprocessing(image.Copy())

    def Preprocessing(self, image: Image) -> Image: ...

    def Like(self, templ: Image) -> bool: ...


element = Scenes


class 可以点击空白处:
    空白处: ClickAction = ClickAction(1, 1)


class 具有返回和主页按钮:
    返回: ClickAction = ClickAction(156, 46)
    大厅: ClickAction = ClickAction(1785, 31)


class __Unknow(可以点击空白处, Scenes):
    def __init__(self) -> None:
        pass

    def Preprocessing(self, image: Image) -> Image:
        return image

    def Like(self, templ: Image) -> bool:
        return True


class __进入游戏(可以点击空白处, Scenes):
    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("进入游戏").Copy())

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((96, 994, 125, 68))

    def Like(self, templ: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)


class __大厅(Scenes):
    工作任务: ClickAction = ClickAction(156, 315)
    邮箱: ClickAction = ClickAction(1655, 56)
    咖啡厅: ClickAction = ClickAction(197, 1000)
    日程: ClickAction = ClickAction(360, 1000)
    成员: ClickAction = ClickAction(525, 1000)
    小组: ClickAction = ClickAction(856, 1000)
    商店: ClickAction = ClickAction(1174, 1000)
    业务区: ClickAction = ClickAction(1736, 875)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("大厅").Copy())

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((1512, 27, 288, 53))

    def Like(self, templ: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)


class __工作任务(具有返回和主页按钮, Scenes):
    class __工作任务X一键领取(ClickableElement, element):
        def __new__(cls):
            return ClickableElement.__new__(cls, 1670, 1008)

        def __init__(self):
            self.src = self.Preprocessing(images.get("工作任务").Copy())

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1546, 977, 237, 68))

        def Like(self, templ: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)

    class __工作任务X领取(ClickableElement, Element):
        def __new__(cls):
            return ClickableElement.__new__(cls, 1419, 1003)

        def __init__(self):
            self.src = self.Preprocessing(images.get("工作任务").Copy())

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1375, 974, 96, 63))

        def Like(self, templ: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)

    一键领取: ClickableElement = __工作任务X一键领取()
    领取: ClickableElement = __工作任务X领取()

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("工作任务").Copy())

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((210, 3, 171, 61))

    def Like(self, templ: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)


class __小组大厅(具有返回和主页按钮, Scenes):
    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("小组大厅").Copy())

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((210, 3, 171, 61))

    def Like(self, templ: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)


class __小组大厅_签到奖励(可以点击空白处, Scenes):
    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("小组大厅").Copy())

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((815, 229, 284, 64))

    def Like(self, templ: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(templ)).IsMax(0.95)


Unknow = __Unknow()
登录_进入游戏 = __进入游戏()
大厅 = __大厅()
小组大厅 = __小组大厅()
小组大厅_签到奖励 = __小组大厅_签到奖励()
工作任务 = __工作任务()
All: list[Scenes] = [
    Unknow,
    登录_进入游戏,
    大厅,
    小组大厅,
    小组大厅_签到奖励,
    工作任务,
]


class Edge:
    frome: Scenes
    to: Scenes

    def __hash__(self) -> int:
        return (str(self.frome) + str(self.to)).__hash__()

    def __init__(self, frome: Scenes, to: Scenes) -> None:
        self.frome = frome
        self.to = to

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Edge):
            return False
        value = cast(Edge, value)
        return value.frome == self.frome and value.to == self.to


class Graph:
    graph: dict[Scenes, list[Scenes]] = {
        登录_进入游戏: [大厅],
        大厅: [小组大厅, 小组大厅_签到奖励, 工作任务],
        小组大厅: [大厅],
        工作任务: [大厅],
    }
    actions: dict[Edge, list[Action]] = {
        Edge(登录_进入游戏, 大厅): [登录_进入游戏.空白处],
        Edge(大厅, 小组大厅): [大厅.小组],
        Edge(大厅, 小组大厅_签到奖励): [大厅.小组],
        Edge(大厅, 工作任务): [大厅.工作任务],
        Edge(小组大厅, 大厅): [小组大厅.返回],
        Edge(工作任务, 大厅): [工作任务.返回],
    }

    def FindPath(self, frome: Scenes, to: Scenes) -> list[Scenes] | None:
        def dfs(start: Scenes, end: Scenes, path: list[Scenes]):
            if start == end:
                return path
            for node in self.graph[start]:
                if node not in path:
                    result = dfs(node, end, path + [node])
                    if result is not None:
                        return result
            return None

        return dfs(frome, to, [frome])

    def FindActions(self, path: list[Scenes]) -> list[list[Action]]:
        result = []
        for i in range(len(path) - 1):
            edge = Edge(path[i], path[i + 1])
            if edge in self.actions:
                result.append(self.actions[edge])
            else:
                # 既然 path 不为 None, 那么必须是可达的
                raise ValueError("path is not reachable")
        return result
