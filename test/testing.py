import cv2
from ba.element import Point, Screen


class TestDrives:
    step = 0
    screen: Screen

    def __init__(self, s: Screen):
        self.screen = s

    def Show(self):
        wait, destry = self.screen.src.Show()
        wait()

    def Click(self, c: Point):
        self.step += 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_thickness = 2

        # 计算文字大小
        (text_width, text_height), baseline = cv2.getTextSize(
            str(self.step), font, font_scale, font_thickness
        )

        # 确保序号不会超出图像边界
        offset = 30  # 文字与点之间的距离
        text_x = c[0] + offset
        text_y = c[1] - offset
        image = self.screen.src.src
        # 调整文本位置以确保不会超出边界
        if text_x + text_width > image.shape[1]:
            text_x = c[0] - text_width - offset
        if text_y - text_height < 0:
            text_y = c[1] + text_height + offset
        self.screen.src.Line(
            c,
            (text_x, text_y - text_height // 2),
            (255, 0, 0),
            2,
        )
        self.screen.src.Point(c, (0, 0, 255), 5)
        self.screen.src.Text(
            str(self.step),
            (text_x, text_y),
            font,
            font_scale,
            (0, 255, 0),
            font_thickness,
        )
