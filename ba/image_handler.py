import time

import cv2

from ba.cv import Image


def start_icon_preprocess_func(img: Image):
    # 右下角 criware 图标
    rect = (1714, 935, 91, 91)
    img.Crop(rect).CvtGray().Threshold(200)


def start_icon_like_func(src: Image, img: Image):
    return src.MatchTemplate(img).IsMax(0.9)


def notice_board_preprocess_func(img: Image):
    # 顶部的蓝色边框
    rect = (656, 146, 1047, 75)
    img.Crop(rect)


def notice_board_like_func(src: Image, img: Image):
    return src.MatchTemplate(img).IsMax(0.9)


def notice_checkbox_preprocess_func(img: Image):
    # 右下角“今日不再显示”选择框
    rect = (1461, 908, 41, 41)
    img.Crop(rect)


def notice_checkbox_like_func(src: Image, img: Image):
    return src.MatchTemplate(img).IsMax(0.9)
