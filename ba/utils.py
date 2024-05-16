from typing import Callable

import numpy as np
from cv2.typing import Point, Rect

from ba.cv import Image


def Distance(p1: Point, p2: Point):
    """计算两点间的欧式距离"""
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def FilterPoint(
    points: list[Point],
    distance_threshold: int,
    filter: Callable[[int, int], bool] = lambda x, y: True,
):
    """过滤掉彼此靠近的点"""
    points = sorted(points, key=lambda point: (point[0], point[1]))
    filtered_points: list[Point] = []

    while points:
        current = points.pop(0)
        if not filter(current[0], current[1]):
            continue
        points = [
            point for point in points if (Distance(point, current) > distance_threshold)
        ]

        filtered_points.append(current)

    return filtered_points


def FindPointInRect(pts: list[Point], rect: Rect) -> Point | None:
    for p in pts:
        if (
            p[0] > rect[0]
            and p[0] < rect[0] + rect[2]
            and p[1] > rect[1]
            and p[1] < rect[1] + rect[3]
        ):
            return p
    return None


def FindRedPoint(img: Image, filter: Callable[[int, int], bool] = lambda x, y: True):
    lower = (5, 210, 230)
    upper = (6, 250, 255)
    pts = (
        img.Copy()
        .InRange(lower, upper)
        .CvtGray()
        .Threshold(100)
        .FindContours()
        .GetCenterPionts()
    )
    return FilterPoint(pts, 30, filter=filter)


def FindYellowPoint(img: Image, filter: Callable[[int, int], bool] = lambda x, y: True):
    lower = (5, 210, 230)
    upper = (6, 250, 255)
    pts = (
        img.Copy()
        .InRange(lower, upper)
        .CvtGray()
        .Threshold(100)
        .FindContours()
        .GetCenterPionts()
    )
    return FilterPoint(pts, 30, filter=filter)
