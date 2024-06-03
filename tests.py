from datetime import timedelta
from typing import Any, ClassVar
import cv2
from ba import game, images, scenes
from ba.element import ClickAction, ElementClickAction, Ocrable, Screen
from ba.scenes import Edge, Graph
from test import testing

testing.IsShowImage = False
for scene in scenes.All:
    s = Screen(images.get(scene.name))
    t = testing.TestDrives(s)
    testing.AssertScene(s, scene)
    for field_name in dir(scene):
        field = getattr(scene, field_name)
        t.Test(field)

    t.Show()


# Graph().Draw("graph.png")
Graph().Show("scens")
