from typing import Iterable, cast

import cv2
from ba import images
from ba.cv import Image
from ba.element import Action, ClickAction, ElementClickAction, Element_
from ba.page import graph


class Scenes(Element_):
    name: str
    src: Image

    def __str__(self) -> str:
        return self.name

    def Preprocessing(self, image: Image) -> Image:
        raise NotImplementedError()

    def Like(self, image: Image) -> bool:
        raise NotImplementedError()


Element = Scenes


class 可以点击空白处:
    空白处: ClickAction = ClickAction("空白处", 1, 1)


class 具有返回和主页按钮:
    返回: ClickAction = ClickAction("返回", 156, 46)
    大厅: ClickAction = ClickAction("大厅", 1785, 31)


class __Unknow(可以点击空白处, Scenes):
    def __init__(self) -> None:
        return

    def Preprocessing(self, image: Image) -> Image:
        return image

    def Like(self, image: Image) -> bool:
        return True


class __登录_通知(可以点击空白处, Scenes):
    name = "登录_通知"
    icon16plus: Image
    title: Image

    def __init__(self) -> None:
        base = self.Preprocessing(images.get("登录_通知"))
        self.icon16plus = base.Copy().Crop((1586, 892, 104, 133))
        self.title = base.Crop((897, 225, 124, 73))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray()

    def Like(self, image: Image) -> bool:
        base = self.Preprocessing(image)
        icon16plus = base.Copy().Crop((1586, 892, 104, 133))
        title = base.Crop((897, 225, 124, 73))
        return self.icon16plus.MatchTemplate(icon16plus).IsMax(
            0.95
        ) and self.title.MatchTemplate(title).IsMax(0.95)


class __登录_进入游戏(可以点击空白处, Scenes):
    name = "登录_进入游戏"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("登录_进入游戏"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((96, 994, 125, 68))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __登录_更新提醒(Scenes):
    name = "登录_更新提醒"
    确认 = ClickAction("确认", 1138, 728)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("登录_更新提醒"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((851, 231, 210, 62))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __大厅(Scenes):
    name = "大厅"
    工作任务: ClickAction = ClickAction("工作任务", 156, 315)
    邮箱: ClickAction = ClickAction("邮箱", 1655, 56)
    全屏大厅: ClickAction = ClickAction("全屏大厅", 1772, 129)
    咖啡厅: ClickAction = ClickAction("咖啡厅", 197, 1000)
    日程: ClickAction = ClickAction("日程", 360, 1000)
    成员: ClickAction = ClickAction("成员", 525, 1000)
    小组: ClickAction = ClickAction("小组", 856, 1000)
    商店: ClickAction = ClickAction("商店", 1174, 1000)
    业务区: ClickAction = ClickAction("业务区", 1736, 875)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("大厅"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((1512, 27, 288, 53)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __工作任务(具有返回和主页按钮, Scenes):
    name = "工作任务"

    class __一键领取(ElementClickAction, Element):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "一键领取", 1670, 1008)

        def __init__(self):
            self.src = self.Preprocessing(images.get("工作任务"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1546, 977, 237, 68))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    class __领取(ElementClickAction, Element):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "领取", 1419, 1003)

        def __init__(self):
            self.src = self.Preprocessing(images.get("工作任务"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1375, 974, 96, 63))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    一键领取: ElementClickAction = __一键领取()
    领取: ElementClickAction = __领取()

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("工作任务"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((210, 3, 171, 61))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __小组大厅(具有返回和主页按钮, Scenes):
    name = "小组大厅"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("小组大厅"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((210, 3, 171, 61))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __小组大厅_签到奖励(可以点击空白处, Scenes):
    name = "小组大厅_签到奖励"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("小组大厅_签到奖励"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((815, 229, 284, 64))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __获得奖励(可以点击空白处, Scenes):
    name = "获得奖励"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("获得奖励"))

    def Preprocessing(self, image: Image) -> Image:
        lower = (50, 0, 0)
        upper = (255, 255, 255)
        return (
            image.Crop((738, 190, 454, 116))
            .InRange(lower, upper)
            .Threshold(0, type=cv2.THRESH_BINARY_INV)
        )

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.8)


class __好感等级提升(可以点击空白处, Scenes):
    name = "好感等级提升"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("好感等级提升"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((716, 899, 447, 81))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.8)


class __大厅_全屏(Scenes):
    name = "大厅_全屏"
    退出全屏 = ClickAction("退出全屏", 1770, 50)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("大厅_全屏"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((1731, 27, 83, 54))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __咖啡厅(具有返回和主页按钮, Scenes):
    name = "咖啡厅"

    class __邀请劵(ElementClickAction, Element):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "邀请劵", 1227, 981)

        def __init__(self):
            self.src = self.Preprocessing(images.get("咖啡厅"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1179, 940, 91, 101))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    class __收益(ElementClickAction, Element):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "收益", 1665, 965)

        def __init__(self):
            self.src = self.Preprocessing(images.get("咖啡厅"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1585, 926, 189, 46))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    邀请劵 = __邀请劵()
    收益 = __收益()

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("咖啡厅"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((215, 1, 276, 58))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __咖啡厅_说明(可以点击空白处, Scenes):
    name = "咖啡厅_说明"
    title: Image
    subTitle: Image

    def __init__(self) -> None:
        base = self.Preprocessing(images.get("咖啡厅_说明"))
        self.title = base.Copy().Crop((215, 1, 276, 58))
        self.subTitle = base.Crop((897, 263, 130, 62))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray()

    def Like(self, image: Image) -> bool:
        base = self.Preprocessing(image)
        title = base.Copy().Crop((215, 1, 276, 58))
        subTitle = base.Crop((897, 263, 130, 62))
        return self.title.MatchTemplate(title).IsMax(
            0.95
        ) and self.subTitle.MatchTemplate(subTitle).IsMax(0.95)


class __咖啡厅_收益(可以点击空白处, Scenes):
    name = "咖啡厅_收益"

    class __领取(ElementClickAction, Element):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "领取", 963, 758)

        def __init__(self):
            self.src = self.Preprocessing(images.get("咖啡厅_收益"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((833, 714, 251, 94))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    领取 = __领取()

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("咖啡厅_收益"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((803, 220, 317, 65))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


Unknow = __Unknow()

登录_通知 = __登录_通知()
登录_进入游戏 = __登录_进入游戏()
登录_更新提醒 = __登录_更新提醒()
大厅 = __大厅()
小组大厅 = __小组大厅()
小组大厅_签到奖励 = __小组大厅_签到奖励()
工作任务 = __工作任务()
获得奖励 = __获得奖励()
好感等级提升 = __好感等级提升()
大厅_全屏 = __大厅_全屏()
咖啡厅 = __咖啡厅()
咖啡厅_收益 = __咖啡厅_收益()
咖啡厅_说明 = __咖啡厅_说明()

All: list[Scenes] = [
    获得奖励,
    登录_通知,
    登录_进入游戏,
    大厅,
    小组大厅,
    小组大厅_签到奖励,
    工作任务,
    好感等级提升,
    大厅_全屏,
    咖啡厅,
    咖啡厅_收益,
    咖啡厅_说明,
    登录_更新提醒,
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
        大厅: [
            小组大厅,
            工作任务,
            大厅_全屏,
            咖啡厅,
        ],
        小组大厅: [大厅],
        工作任务: [大厅],
        大厅_全屏: [大厅],
        咖啡厅: [大厅, 咖啡厅_收益],
        咖啡厅_收益: [咖啡厅],
        咖啡厅_说明: [咖啡厅],
    }
    actions: dict[Edge, list[Action]] = {
        Edge(登录_进入游戏, 大厅): [登录_进入游戏.空白处],
        Edge(大厅, 小组大厅): [大厅.小组],
        Edge(大厅, 工作任务): [大厅.工作任务],
        Edge(大厅, 大厅_全屏): [大厅.全屏大厅],
        Edge(大厅, 咖啡厅): [大厅.咖啡厅],
        Edge(大厅, 咖啡厅_说明): [大厅.咖啡厅],
        Edge(大厅_全屏, 大厅): [大厅_全屏.退出全屏],
        Edge(小组大厅, 大厅): [小组大厅.返回],
        Edge(工作任务, 大厅): [工作任务.返回],
        Edge(咖啡厅, 大厅): [咖啡厅.返回],
        Edge(咖啡厅, 咖啡厅_收益): [咖啡厅.收益],
        Edge(咖啡厅_收益, 咖啡厅): [咖啡厅_收益.空白处],
        Edge(咖啡厅_说明, 咖啡厅): [咖啡厅_说明.空白处],
    }

    def Draw(self, chineseFont: str, file: str):
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.DiGraph()
        for vertex in self.graph:
            G.add_node(vertex)
        for from_vertex in self.graph:
            for to_vertex in self.graph[from_vertex]:
                G.add_edge(from_vertex, to_vertex)

        pos = nx.spring_layout(G)
        cf = plt.gcf()
        cf.set_facecolor("w")
        ax = cf.add_axes((0, 0, 1, 1))
        ax.set_axis_off()
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=3000, alpha=0.2)
        nx.draw_networkx_labels(G, pos, font_family=chineseFont)

        edgeLabels = {}
        for a in self.actions:
            lsbel = ""
            for action in self.actions[a]:
                lsbel = action.type.value + ":" + str(action)
            edgeLabels[(a.frome, a.to)] = lsbel
        for from_vertex in self.graph:
            for to_vertex in self.graph[from_vertex]:
                rad = 0.3
                connectionstyle = f"arc3,rad={rad if (from_vertex, to_vertex) in edgeLabels and (to_vertex, from_vertex) in edgeLabels else 0}"
                label = edgeLabels[(from_vertex, to_vertex)]
                arrow = nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=[(from_vertex, to_vertex)],
                    arrowstyle="-|>",
                    style="solid",
                    connectionstyle=connectionstyle,
                    edge_color="black",
                    arrowsize=20,
                    min_target_margin=15,
                    node_size=3000,
                )[0]
                # 计算曲线边的中点
                path = arrow.get_path()
                path_transform = arrow.get_transform()
                path_data = path.interpolated(100).vertices
                midpoint = path_data[len(path_data) // 6]
                # 添加边的标签
                plt.text(
                    midpoint[0],
                    midpoint[1],
                    label,
                    color="red",
                    ha="center",
                    va="center",
                    fontsize=8,
                    transform=path_transform,
                    font=chineseFont,
                )

        plt.savefig(file)

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
