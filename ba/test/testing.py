import cv2
from ba.element import Point, Screen


class TestDrives:
    step = 0
    screen: Screen

    def SetScreen(self, s: Screen):
        self.screen = s

    def Show(self):
        self.screen.src.Show()

    def Click(self, c: Point):
        # self.screen.src.Circle(c, 3, (255, 0, 0))

        point = (250, 250)
        index = 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1

        # 计算文字大小
        (text_width, text_height), baseline = cv2.getTextSize(
            str(index), font, font_scale, font_thickness
        )

        # 确保序号不会超出图像边界
        offset = 10  # 文字与点之间的距离
        text_x = point[0] + offset
        text_y = point[1] - offset
        image = self.screen.src.src
        # 调整文本位置以确保不会超出边界
        if text_x + text_width > image.shape[1]:
            text_x = point[0] - text_width - offset
        if text_y - text_height < 0:
            text_y = point[1] + text_height + offset
        cv2.line(image, point, (text_x, text_y - text_height // 2), (255, 0, 0), 1)

        cv2.putText(
            image,
            str(index),
            (text_x, text_y),
            font,
            font_scale,
            (255, 255, 255),
            font_thickness,
        )
