import re
import time
import types
from types import EllipsisType
from typing import Callable, cast

import cv2
import cv2.typing as cvtypes
import numpy as np
from PIL import Image as PILImage


def NonMaxSuppression(
    points: list[tuple[int, int]], scores, threshold: float
) -> list[tuple[int, int]]:
    if len(points) == 0:
        return []

    # 将点和得分按得分从高到低排序
    idxs = np.argsort(scores)[::-1]
    sorted_points = [points[i] for i in idxs]

    suppressed = [False] * len(points)
    result = []

    for i in range(len(sorted_points)):
        if suppressed[i]:
            continue
        result.append(sorted_points[i])
        for j in range(i + 1, len(sorted_points)):
            if (
                not suppressed[j]
                and np.linalg.norm(
                    np.array(sorted_points[i]) - np.array(sorted_points[j])
                )
                < threshold
            ):
                suppressed[j] = True

    return result


# 用于处理模板匹配的结果
class MatchImage:
    result: cvtypes.MatLike
    shape: cv2.typing.MatShape

    def __init__(self, shape: cv2.typing.MatShape, result: cvtypes.MatLike) -> None:
        self.result = result
        self.shape = shape

    def Max(self, mask: cvtypes.MatLike | None = None):
        _, max_val, _, max_loc = cv2.minMaxLoc(self.result, mask)
        return max_val, max_loc

    def Min(self, mask: cvtypes.MatLike | None = None):
        min_val, _, min_loc, _ = cv2.minMaxLoc(self.result, mask)
        return min_val, min_loc

    def IsMax(self, threshold: float, mask: cvtypes.MatLike | None = None):
        val, _ = self.Max(mask)
        return val > threshold

    def IsMin(self, threshold: float, mask: cvtypes.MatLike | None = None):
        val, _ = self.Min(mask)
        return val < threshold

    def BigThan(self, threshold: float, mask: cvtypes.MatLike | None = None):
        loc = np.where(self.result >= threshold)  # type: ignore
        pts = list(zip(*loc[::-1]))
        scores = self.result[loc]
        nms_threshold = min(self.shape) / 2
        return NonMaxSuppression(pts, scores, nms_threshold)

    def SmallThan(self, threshold: float, mask: cvtypes.MatLike | None = None):
        loc = np.where(self.result <= threshold)  # type: ignore
        pts = list(zip(*loc[::-1]))
        scores = self.result[loc]
        nms_threshold = min(self.shape) / 2
        return NonMaxSuppression(pts, scores, nms_threshold)


class SplitSelect:
    __b: Callable[[], "Image"]
    __g: Callable[[], "Image"]
    __r: Callable[[], "Image"]
    __a: Callable[[], "Image"]

    def __init__(self, b, g, r, a):
        self.__b = b
        self.__g = g
        self.__r = r
        self.__a = a

    def B(self):
        return self.__b()

    def G(self):
        return self.__g()

    def R(self):
        return self.__r()

    def A(self):
        return self.__a()


class Image:
    src: cvtypes.MatLike
    __origin: cvtypes.MatLike
    precessFunc: Callable[["Image"], None] = lambda self: None

    def __init__(
        self,
        image: bytes | cvtypes.MatLike,
        flag: int = cv2.IMREAD_COLOR,
        preprocessFunc: Callable[["Image"], None] | None = None,
    ) -> None:
        """
        preprocessFunc 是预处理函数，将在 __init__ 内调用
        """
        if isinstance(image, bytes):
            image_array = np.frombuffer(image, np.uint8)
            self.src = cv2.imdecode(image_array, flag)
        else:
            self.src = cast(cvtypes.MatLike, image).copy()
        if preprocessFunc:
            self.precessFunc = preprocessFunc
            preprocessFunc(self)
        self.__origin = self.src.copy()  # type: ignore

    def ToPillowImage(self) -> PILImage.Image:
        return PILImage.fromarray(self.src)

    def Reset(self):
        self.src = self.__origin.copy()
        return self

    def Save(self, name: str):
        cv2.imwrite(name, self.src)
        return self

    def Copy(self) -> "Image":
        i = Image(self.src.copy())
        i.precessFunc = self.precessFunc
        return i

    def Size(self) -> cvtypes.Size:
        """(width, height)"""
        return self.src.shape[1], self.src.shape[0]

    def Show(
        self, windowName: str = "Image"
    ) -> tuple[Callable[[], None], Callable[[], None]]:
        cv2.imshow(windowName, self.src)

        def destory():
            cv2.destroyWindow(windowName)

        def wait():
            while True:
                key = cv2.waitKey(0) & 0xFF
                if key == 27:  # ESC键的值为27
                    destory()
                    break

        return wait, destory

    def Threshold(
        self,
        thresh: float,
        maxval: float = 255,
        type: int = cv2.THRESH_BINARY,
    ):
        _, self.src = cv2.threshold(self.src, thresh, maxval, type)
        return self

    def Split(self, index: int, useGray: bool = True):
        sp = cv2.split(self.src)
        if not useGray:
            zeros = np.zeros(self.src.shape[:2], dtype="uint8")
            if index == 0:
                self.src = cv2.merge([sp[0], zeros, zeros])
            if index == 1:
                self.src = cv2.merge([zeros, sp[1], zeros])
            if index == 2:
                self.src = cv2.merge([zeros, zeros, sp[2]])
            if index == 3:
                self.src = cv2.merge([sp[0], sp[1], sp[2], sp[4]])
        else:
            self.src = sp[index]
        return self

    def CvtColor(self, code: int):
        result = cv2.cvtColor(self.src, code)

        class select:
            __img: Image
            Result: cvtypes.MatLike

            def __init__(self, img, result) -> None:
                self.__img = img
                self.Result = result

            def Apply(self):
                self.__img.src = self.Result
                return self.__img

            def NewImage(self) -> Image:
                return Image(self.Result)

        return select(self, result)

    def CvtGray(self):
        return self.CvtColor(cv2.COLOR_BGR2GRAY).Apply()

    def Resize(
        self,
        dsize: cvtypes.Size | None = None,
        fx: float | EllipsisType = ...,
        fy: float | EllipsisType = ...,
        interpolation: int = cv2.INTER_LINEAR,
    ):
        self.src = cv2.resize(
            self.src,
            dsize,
            self.src,
            fx,  # type: ignore
            fy,  # type: ignore
            interpolation,
        )  # type: ignore
        return self

    def EqualizeHist(self):
        cv2.equalizeHist(self.src, self.src)
        return self

    def Blur(self, ksize: cvtypes.Size):
        cv2.blur(self.src, ksize, self.src)
        return self

    def GaussianBlur(self, ksize: cvtypes.Size, sigmaX: float = 0, sigmaY: float = 0):
        self.src = cv2.GaussianBlur(self.src, ksize, sigmaX=sigmaX, sigmaY=sigmaY)
        return self

    def MedianBlur(self, ksize: int):
        self.src = cv2.medianBlur(self.src, ksize)
        return self

    def BilateralFilter(
        self,
        d: int,
        sigmaColor: float,
        sigmaSpace: float,
        borderType: int = cv2.BORDER_REPLICATE,
    ):
        self.src = cv2.bilateralFilter(
            self.src, d, sigmaColor, sigmaSpace, borderType=borderType
        )
        return self

    def Sobel(
        self,
        ddepth: int,
        dx: int,
        dy: int,
        ksize: int | EllipsisType = ...,
        scale: float | EllipsisType = ...,
        delta: float | EllipsisType = ...,
        borderType: int | EllipsisType = ...,
    ):
        self.src = cv2.Sobel(
            self.src,
            ddepth,
            dx,
            dy,
            ksize=ksize,  # type: ignore
            scale=scale,  # type: ignore
            delta=delta,  # type: ignore
            borderType=borderType,  # type: ignore
        )  # type: ignore
        return self

    def MatchTemplate(
        self,
        image: cvtypes.MatLike | "Image",
        method: int = cv2.TM_CCOEFF_NORMED,
        mask: cvtypes.MatLike | None = None,
    ):
        """将自身作为模版进行模板匹配"""
        tpl: cvtypes.MatLike
        if type(image) == cvtypes.MatLike:
            tpl = cast(cvtypes.MatLike, image)
        else:
            tpl = cast(Image, image).src
        res = cv2.matchTemplate(tpl, self.src, method, None, mask)
        return MatchImage(self.src.shape, res)

    def Rectangle(
        self,
        pt1: cvtypes.Point,
        pt2: cvtypes.Point,
        color: cvtypes.Scalar,
        thickness: int = 1,
        lineType: int = 0,
        shift: int = 0,
    ):
        self.src = cv2.rectangle(
            self.src,
            pt1=pt1,
            pt2=pt2,
            color=color,
            thickness=thickness,
            lineType=lineType,
            shift=shift,  # type: ignore
        )  # type: ignore
        return self

    def Circle(
        self,
        center: cvtypes.Point,
        radius: int,
        color: cvtypes.Scalar,
        thickness: int = 1,
        lineType: int = 0,
        shift: int = 0,
    ):
        self.src = cv2.circle(
            self.src,
            center=center,
            radius=radius,
            color=color,
            thickness=thickness,
            lineType=lineType,
            shift=shift,
        )
        return self

    def Point(self, point: cvtypes.Point, color: cvtypes.Scalar, radius: int):
        self.src = cv2.circle(self.src, point, radius, color, -1)
        return self

    def Text(
        self,
        text: str,
        org: cvtypes.Point,
        fontFace: int,
        fontScale: float,
        color: cvtypes.Scalar,
        thickness: int = 2,
        lineType: int = 2,
        bottomLeftOrigin: bool = False,
    ):
        self.src = cv2.putText(
            self.src,
            text,
            org,
            fontFace,
            fontScale,
            color,
            thickness,
            lineType,
            bottomLeftOrigin,
        )
        return self

    def Line(
        self,
        pt1: cvtypes.Point,
        pt2: cvtypes.Point,
        color: cvtypes.Scalar,
        thickness: int = 2,
        lineType: int = 1,
        shift: int = 0,
    ):
        self.src = cv2.line(self.src, pt1, pt2, color, thickness, lineType, shift)
        return self

    def Crop(self, rect: cvtypes.Rect):
        """裁剪自身

        Args:
            rect (Rect): [x, y, width, height]
        """

        self.src = self.src[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]
        return self

    def Cut(self, rect: cvtypes.Rect):
        """裁剪图像, 返回被裁剪的图像

        Args:
            rect (Rect): [x, y, width, height]
        """

        return Image(self.src[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]])

    def Rotate(self, angle: int, scale: int = 1, center: cvtypes.Point2f | None = None):
        """逆时针旋转"""
        _center: cvtypes.Point2f
        size = self.Size()
        if not center:
            # 设置旋转中心为图像中心
            _center = cast(cvtypes.Point2f, (size[0] / 2, size[1] / 2))
        else:
            _center = center
        M = cv2.getRotationMatrix2D(_center, angle, scale)
        self.src = cv2.warpAffine(self.src, M, size)
        return self

    def InRange(
        self,
        lower: tuple[int, int, int],
        upper: tuple[int, int, int],
        hsv_src: cvtypes.MatLike | None = None,
    ):
        if hsv_src is None:
            hsv_src = cv2.cvtColor(self.src, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_src, np.array(lower), np.array(upper))
        self.src = cv2.bitwise_and(self.src, self.src, mask=mask)
        return self

    def FindContours(
        self, mode: int = cv2.RETR_EXTERNAL, method: int = cv2.CHAIN_APPROX_SIMPLE
    ):
        contours, hierarchy = cv2.findContours(self.src, mode, method)

        class con:
            contours: list[np.ndarray]
            hierarchy: np.ndarray
            img: Image

            def __init__(self, img, contours, hierarchy) -> None:
                self.img = img
                self.contours = contours
                self.hierarchy = hierarchy

            def Drow(
                self,
                img: Image | None = None,
                contourIdx: int = -1,
                color: cvtypes.Scalar = (255, 255, 255),
                thickness: int = 3,
            ):
                _img = self.img
                if img is not None:
                    _img = img
                _img.src = cv2.drawContours(
                    self.img.src,
                    self.contours,
                    contourIdx=contourIdx,
                    color=color,
                    thickness=thickness,
                )
                return _img

            def DrowRect(
                self,
                img: Image | None = None,
                border: int = 0,
                color: cvtypes.Scalar = (255, 255, 255),
                thickness: int = 3,
            ):
                _img = self.img
                if img is not None:
                    _img = img
                for contour in self.contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    _img.Rectangle(
                        (x - border, y - border),
                        (x + w + border, y + h + border),
                        color,
                        thickness,
                    )

                return _img

            def GetCenterPionts(self):
                result: list[cvtypes.Point] = []
                for contour in self.contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    result.append((x + w // 2, y + h // 2))
                return result

        return con(self, contours, hierarchy)


EmptyImage = Image(np.zeros((128, 512, 3), np.uint8))
