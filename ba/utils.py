import functools
import time
from typing import Callable, cast

import numpy as np
from cv2.typing import Rect

from ba.cv import Image

Point = tuple[int, int]


def Timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算运行时间
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result

    return wrapper


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
    return FilterPoint(cast(list[Point], pts), 30, filter=filter)


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
    return FilterPoint(cast(list[Point], pts), 30, filter=filter)
