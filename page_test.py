import cv2
import numpy as np

import ba
from ba.cv import Image

with open("主页.png", "rb") as f:
    img = Image(f.read())

from ba.utils import FindRedPoint, FindYellowPoint

pts = FindRedPoint(img)

for p in pts:
    img.Circle(p, 10, (0, 255, 0), 2)

wait, _ = img.Show()
wait()
