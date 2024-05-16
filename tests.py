from ba import scenes
from ba.scenes import Edge
from test import scenes as tscenes

e1 = Edge(scenes.进入游戏, scenes.大厅)
e2 = Edge(scenes.进入游戏, scenes.大厅)
e3 = Edge(scenes.大厅, scenes.进入游戏)
print(e1 == e2)
print(e2 == e3)
g = scenes.Graph()
path = g.FindPath(scenes.进入游戏, scenes.小组大厅)
p = g.FindActions(path)
print(p)
# tscenes.进入游戏.test()
# tscenes.大厅.test()
