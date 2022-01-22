# coding: utf-8
# author: zpt
"""新图片验证码 五位字符"""
import base64
import os
import random
from io import BytesIO
from typing import Union, Optional

from PIL import Image, ImageFont, ImageDraw
# python -m pip install Pillow
from PIL.PngImagePlugin import PngImageFile
import torchvision.transforms as transforms

from cms import settings
from libs.utils.unique_enum import UniqueIntEnum


class CaptchaTypeEnum(UniqueIntEnum):
    """
    功能说明：验证码类型枚举类
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2021-03-03     new
    -------------------------------
    """
    BILL_APP: int = 0  # APP
    BILL_WEB: int = 1  # WEB


# 创建图片的高度和宽度
WIDTH = 160
HEIGHT = 50
WIDTH_TYPE_INFO_DICT = {
    CaptchaTypeEnum.BILL_APP: 218,
    CaptchaTypeEnum.BILL_WEB: 160
}

HEIGHT_TYPE_INFO_DICT = {
    CaptchaTypeEnum.BILL_APP: 50,
    CaptchaTypeEnum.BILL_WEB: 50
}


class NewImageCaptchaHandler(object):
    """
    功能说明：新的图片验证码操作类
    --------------------------------------------
    修改人        修改时间        修改原因
    --------------------------------------------
    zpt          2021-11-13      new
    --------------------------------------------
    """

    # 设置字体路径
    font_dir: str = os.path.join(settings.BASE_DIR, 'static', 'font')

    @property
    def get_random_char(self) -> str:
        """生成随机的子母（大写小写）和数字"""
        random_num = str(random.randint(0, 9))
        random_lower = chr(random.randint(97, 122))  # 小写字母a~z
        random_upper = chr(random.randint(65, 90))  # 大写字母A~Z
        random_char = random.choice([random_num, random_lower, random_upper])
        return random_char

    @property
    def rgb_color(self) -> tuple:
        """随机生成RGB的色彩值"""
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return red, green, blue

    def create_line(self, draw) -> None:
        """绘制线条"""
        for i in range(10):
            x1 = random.randint(0, WIDTH)
            x2 = random.randint(0, WIDTH)
            y1 = random.randint(0, HEIGHT)
            y2 = random.randint(0, HEIGHT)
            draw.line((x1, y1, x2, y2), fill=self.rgb_color, width=2)
        return None

    def create_point(self, draw) -> None:
        """绘制随机点"""
        for i in range(50):
            x_point = random.randint(0, WIDTH)
            y_point = random.randint(0, HEIGHT)
            draw.point((x_point, y_point), fill=self.rgb_color)
        return None

    def image_transform_into_context(self, image: Optional[PngImageFile]):
        """输出图片转为tensor后的格式"""
        # 转为tensor
        input_transform = transforms.Compose([transforms.ToTensor()])

        image = input_transform(image).unsqueeze(0)
        # 输出图片转为tensor后的格式
        print("image_tensor: ", image.shape)

    def create_code_image(self) -> Union[tuple, None]:
        """创建图片验证码"""
        font_path: str = os.path.join(self.font_dir, 'HGKT_CNKI.TTF')
        background_color = self.rgb_color
        # 创建一张随机的背景图片
        img = Image.new(mode="RGB", size=(WIDTH, HEIGHT), color=background_color)
        # 设置文字的字体
        # font = ImageFont.truetype(font="ahellya.ttf", size=36)
        font = ImageFont.truetype(font=font_path, size=36)
        # 图片画笔进行绘制图片
        draw = ImageDraw.Draw(img)
        # 随机生成5位验证码
        str_data = ""
        for index in range(5):

            str_or_num = self.get_random_char
            text_color = self.rgb_color
            # 防止背景的颜色和字体的颜色一致
            while text_color == background_color:
                text_color = self.rgb_color
            # draw.text()  第一个参数为参数在图片上的坐标
            draw.text((10 + 30 * index, 3), text=str_or_num, fill=text_color, font=font)
            str_data += str_or_num
        # print(str_data)  # 生成的验证码
        # self.create_line(draw)
        self.create_point(draw)
        # img.show()
        # 保存
        # img.save("zpt.png")
        # self.image_transform_into_context(image=img)
        # image = Image.open("zpt.png")
        # print(image.info)
        image = BytesIO()
        img.save(image, "png")
        data = image.getvalue()
        # base64编码
        data = base64.b64encode(data).decode("utf-8")

        return str_data, data
