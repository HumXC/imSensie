import random
from typing import cast
from collections import deque
import cv2
from ba import images
from ba.cv import Image
from ba.element import Action, ClickAction, ElementClickAction, Element as Element


class BaseElement(Element):
    name: str

    def __str__(self) -> str:
        return self.name

    def Preprocessing(self, image: Image) -> Image:
        raise NotImplementedError()

    def Like(self, image: Image) -> bool:
        raise NotImplementedError()


class 可以点击空白处:
    空白处 = ClickAction("空白处", 1, 1)


class 具有返回和主页按钮:
    返回 = ClickAction("返回", 156, 46)
    大厅 = ClickAction("大厅", 1785, 31)


class __Unknow(可以点击空白处, BaseElement):
    def __init__(self) -> None:
        return

    def Preprocessing(self, image: Image) -> Image:
        return image

    def Like(self, image: Image) -> bool:
        return True


class __登录_通知(可以点击空白处, BaseElement):
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


class __登录_进入游戏(可以点击空白处, BaseElement):
    name = "登录_进入游戏"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("登录_进入游戏"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((96, 994, 125, 68))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __登录_更新提醒(BaseElement):
    name = "登录_更新提醒"
    确认 = ClickAction("确认", 1138, 728)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("登录_更新提醒"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((851, 231, 210, 62))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __大厅(BaseElement):
    name = "大厅"
    工作任务 = ClickAction("工作任务", 156, 315)
    邮箱 = ClickAction("邮箱", 1655, 56)
    全屏大厅 = ClickAction("全屏大厅", 1772, 129)
    咖啡厅 = ClickAction("咖啡厅", 197, 1000)
    日程 = ClickAction("日程", 360, 1000)
    成员 = ClickAction("成员", 525, 1000)
    小组 = ClickAction("小组", 856, 1000)
    商店 = ClickAction("商店", 1174, 1000)
    业务区 = ClickAction("业务区", 1736, 875)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("大厅"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((1512, 27, 288, 53)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __工作任务(具有返回和主页按钮, BaseElement):
    name = "工作任务"

    class __一键领取(ElementClickAction, BaseElement):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "一键领取", 1670, 1008)

        def __init__(self):
            self.src = self.Preprocessing(images.get("工作任务"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1546, 977, 237, 68))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    class __领取(ElementClickAction, BaseElement):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "领取", 1419, 1003)

        def __init__(self):
            self.src = self.Preprocessing(images.get("工作任务"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1375, 974, 96, 63))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    一键领取 = __一键领取()
    领取 = __领取()

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("工作任务"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((210, 3, 171, 61)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __小组大厅(具有返回和主页按钮, BaseElement):
    name = "小组大厅"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("小组大厅"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((210, 3, 171, 61)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __小组大厅_签到奖励(可以点击空白处, BaseElement):
    name = "小组大厅_签到奖励"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("小组大厅_签到奖励"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((815, 229, 284, 64))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __获得奖励(BaseElement):
    name = "获得奖励"
    继续 = ClickAction("继续", 968, 957)

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


class __好感等级提升(可以点击空白处, BaseElement):
    name = "好感等级提升"

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("好感等级提升"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((716, 899, 447, 81))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.8)


class __大厅_全屏(BaseElement):
    name = "大厅_全屏"
    退出全屏 = ClickAction("退出全屏", 1770, 50)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("大厅_全屏"))

    def Preprocessing(self, image: Image) -> Image:
        return image.CvtGray().Crop((1731, 27, 83, 54))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __咖啡厅(具有返回和主页按钮, BaseElement):
    name = "咖啡厅"

    class __邀请劵(ElementClickAction, BaseElement):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "邀请劵", 1227, 981)

        def __init__(self):
            self.src = self.Preprocessing(images.get("咖啡厅"))

        def Preprocessing(self, image: Image) -> Image:
            return image.Crop((1179, 940, 91, 101))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    class __收益(ElementClickAction, BaseElement):
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
        return image.Crop((215, 1, 276, 58)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __咖啡厅_说明(可以点击空白处, BaseElement):
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


class __咖啡厅_收益(可以点击空白处, BaseElement):
    name = "咖啡厅_收益"

    class __领取(ElementClickAction, BaseElement):
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
        return image.Crop((803, 220, 317, 65))

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __邮箱(具有返回和主页按钮, BaseElement):
    name = "邮箱"

    class __一键领取(ElementClickAction, BaseElement):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "一键领取", 1648, 1006)

        def __init__(self):
            self.src = self.Preprocessing(images.get("邮箱"))

        def Preprocessing(self, image: Image) -> Image:
            return image.CvtGray().Crop((1534, 969, 221, 81))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    一键领取 = __一键领取()

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("邮箱"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((197, 0, 126, 62)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __业务区(具有返回和主页按钮, BaseElement):
    name = "业务区"
    任务 = ClickAction("任务", 1201, 414)
    故事 = ClickAction("故事", 1591, 410)
    悬赏通缉 = ClickAction("悬赏通缉", 1100, 631)
    特别委托 = ClickAction("特别委托", 1071, 744)
    学院交流会 = ClickAction("学院交流会", 1064, 858)
    总力战 = ClickAction("总力战", 1064, 858)
    战术综合测试 = ClickAction("战术综合测试", 1321, 838)
    战术对抗赛 = ClickAction("战术对抗赛", 1591, 754)

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("业务区"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((211, 3, 135, 58)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

    def Like(self, image: Image) -> bool:
        return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)


class __战术对抗赛(具有返回和主页按钮, BaseElement):
    name = "战术对抗赛"

    class __时间奖励(ElementClickAction, BaseElement):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "时间奖励", 558, 585)

        def __init__(self):
            self.src = self.Preprocessing(images.get("战术对抗赛"))

        def Preprocessing(self, image: Image) -> Image:
            return image.CvtGray().Crop((478, 525, 171, 97))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    class __每日奖励(ElementClickAction, BaseElement):
        def __new__(cls):
            return ElementClickAction.__new__(cls, "每日奖励", 558, 686)

        def __init__(self):
            self.src = self.Preprocessing(images.get("战术对抗赛"))

        def Preprocessing(self, image: Image) -> Image:
            return image.CvtGray().Crop((482, 644, 162, 83))

        def Like(self, image: Image) -> bool:
            return self.src.MatchTemplate(self.Preprocessing(image)).IsMax(0.95)

    时间奖励 = __时间奖励()
    每日奖励 = __每日奖励()

    def __init__(self) -> None:
        self.src = self.Preprocessing(images.get("战术对抗赛"))

    def Preprocessing(self, image: Image) -> Image:
        return image.Crop((211, 3, 135, 58)).CvtColor(cv2.COLOR_BGR2HLS).Apply()

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
邮箱 = __邮箱()
业务区 = __业务区()
战术对抗赛 = __战术对抗赛()
All: list[BaseElement] = [
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
    邮箱,
    业务区,
    战术对抗赛,
]


class Edge:
    frome: Element
    to: Element

    def __hash__(self) -> int:
        return (str(self.frome) + str(self.to)).__hash__()

    def __init__(self, frome: Element, to: Element) -> None:
        self.frome = frome
        self.to = to

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Edge):
            return False
        value = cast(Edge, value)
        return value.frome == self.frome and value.to == self.to


class Graph:
    graph: dict[Element, list[Element]] = {
        登录_进入游戏: [大厅],
        大厅: [
            小组大厅,
            工作任务,
            大厅_全屏,
            咖啡厅,
            邮箱,
            业务区,
        ],
        小组大厅: [大厅],
        工作任务: [大厅, 获得奖励],
        大厅_全屏: [大厅],
        咖啡厅: [大厅, 咖啡厅_收益],
        咖啡厅_收益: [咖啡厅, 获得奖励],
        咖啡厅_说明: [咖啡厅],
        邮箱: [大厅, 获得奖励],
        业务区: [大厅, 战术对抗赛],
        战术对抗赛: [业务区, 获得奖励, 大厅],
    }
    actions: dict[Edge, list[Action]] = {
        Edge(登录_进入游戏, 大厅): [登录_进入游戏.空白处],
        Edge(大厅, 小组大厅): [大厅.小组],
        Edge(大厅, 工作任务): [大厅.工作任务],
        Edge(大厅, 大厅_全屏): [大厅.全屏大厅],
        Edge(大厅, 咖啡厅): [大厅.咖啡厅],
        Edge(大厅, 咖啡厅_说明): [大厅.咖啡厅],
        Edge(大厅, 邮箱): [大厅.邮箱],
        Edge(大厅, 业务区): [大厅.业务区],
        Edge(大厅_全屏, 大厅): [大厅_全屏.退出全屏],
        Edge(小组大厅, 大厅): [小组大厅.返回],
        Edge(工作任务, 大厅): [工作任务.返回],
        Edge(工作任务, 获得奖励): [工作任务.一键领取, 工作任务.领取],
        Edge(咖啡厅, 大厅): [咖啡厅.返回],
        Edge(咖啡厅, 咖啡厅_收益): [咖啡厅.收益],
        Edge(咖啡厅_收益, 咖啡厅): [咖啡厅_收益.空白处],
        Edge(咖啡厅_收益, 获得奖励): [咖啡厅_收益.领取],
        Edge(咖啡厅_说明, 咖啡厅): [咖啡厅_说明.空白处],
        Edge(邮箱, 获得奖励): [邮箱.一键领取],
        Edge(邮箱, 大厅): [邮箱.返回],
        Edge(业务区, 大厅): [业务区.返回],
        Edge(业务区, 战术对抗赛): [业务区.战术对抗赛],
        Edge(战术对抗赛, 业务区): [战术对抗赛.返回],
        Edge(战术对抗赛, 获得奖励): [战术对抗赛.每日奖励, 战术对抗赛.时间奖励],
        Edge(战术对抗赛, 大厅): [战术对抗赛.大厅],
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
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        cf = plt.gcf()
        cf.set_facecolor("black")
        ax = cf.add_axes((0, 0, 1, 1))
        ax.set_axis_off()
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=3000, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_family=chineseFont, font_color="white")

        edgeLabels = {}
        for a in self.actions:
            label = ""
            for action in self.actions[a]:
                label += "\n" + action.type.value + ":" + str(action)
            label = label[1:]
            edgeLabels[(a.frome, a.to)] = label
        colors = [
            "#1f77b4",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
            "#ff7f0e",
            "#393b79",
            "#637939",
            "#8c6d31",
            "#843c39",
            "#7b4173",
            "#5254a3",
            "#6b6ecf",
            "#9c9ede",
            "#8ca252",
            "#b5cf6b",
            "#cedb9c",
            "#bd9e39",
            "#e7ba52",
            "#e7969c",
            "#de9ed6",
            "#ad494a",
            "#d6616b",
            "#e7cb94",
            "#7b4173",
            "#a55194",
            "#ce6dbd",
        ]

        for from_vertex in self.graph:
            for to_vertex in self.graph[from_vertex]:
                color = random.choice(colors)
                rad = 0.3
                connectionstyle = f"arc3,rad={rad if (from_vertex, to_vertex) in edgeLabels and (to_vertex, from_vertex) in edgeLabels else 0}"
                label = edgeLabels[(from_vertex, to_vertex)]
                arrow = nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=[(from_vertex, to_vertex)],
                    arrowstyle="-|>",
                    style="dashed",
                    connectionstyle=connectionstyle,
                    edge_color=color,
                    arrowsize=20,
                    min_target_margin=15,
                    node_size=3000,
                    edge_vmin=100,
                )[0]
                # 计算曲线边的中点
                path = arrow.get_path()
                path_transform = arrow.get_transform()
                path_data = path.interpolated(200).vertices
                midpoint = path_data[len(path_data) // 5]

                plt.text(
                    midpoint[0],
                    midpoint[1],
                    label,
                    color=color,
                    ha="center",
                    va="center",
                    fontsize=8,
                    transform=path_transform,
                    font=chineseFont,
                )

        plt.savefig(file, dpi=600)

    def FindPath(self, start: Element, end: Element) -> list[Element] | None:
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == end:
                return path

            if node not in visited:
                visited.add(node)
                for neighbor in self.graph.get(node, []):
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None

    def FindActions(self, path: list[Element]) -> list[list[Action]]:
        result = []
        for i in range(len(path) - 1):
            edge = Edge(path[i], path[i + 1])
            if edge in self.actions:
                result.append(self.actions[edge])
            else:
                # 既然 path 不为 None, 那么必须是可达的
                raise ValueError("path is not reachable")
        return result
