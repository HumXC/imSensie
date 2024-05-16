from abc import ABC, abstractmethod
from typing import Callable


class node:
    name: str
    # 邻居
    neighbors: dict[str, "node"]

    # @abstractmethod
    # def IsLike(self) -> bool:
    #     pass

    # @abstractmethod
    # def Go(self) -> bool:
    #     pass
    def add_neighbor(self, node_name: str, node: "node"):
        self.neighbors[node_name] = node


class start(node):
    name: str = "start"


class home(node):
    name: str = "home"


class notice(node):
    name: str = "notice"


class graph:
    Start = start()
    Home = home()
    Notice = notice()

    def __init__(self) -> None:
        # start 页面确实能够跳转到这3个页面，但是是不确定的
        self.Start.add_neighbor("home", self.Home)
        self.Start.add_neighbor("notice", self.Notice)

        self.Notice.add_neighbor("home", self.Home)

        self.Home.add_neighbor("notice", self.Notice)
