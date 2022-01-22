# coding: utf-8

import random
from captcha.image import ImageCaptcha, ImageFilter


class ICaptcha(ImageCaptcha):
    """
    功能说明：图片验证码扩展类
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    ld          2021-04-08      new
    ------------------------------------
    """

    def __init__(self, font_color=None, background_color=None, *args, **kwargs):
        super(ICaptcha, self).__init__(*args, **kwargs)
        self._font_color = font_color
        self._background_color = background_color

    @staticmethod
    def random_color(start, end, opacity=None):
        red = random.randint(start, end)
        green = random.randint(start, end)
        blue = random.randint(start, end)
        if opacity is None:
            return red, green, blue
        return red, green, blue, opacity

    def generate_image(self, chars):
        background = self._background_color or self.random_color(238, 255)
        color = self._font_color or self.random_color(10, 200, random.randint(220, 255))
        im = self.create_captcha_image(chars, color, background)
        # self.create_noise_dots(im, color)
        # self.create_noise_curve(im, color)
        # im = im.filter(ImageFilter.SMOOTH)
        # im = im.filter(ImageFilter.EDGE_ENHANCE)
        # im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # im = im.filter(ImageFilter.SMOOTH_MORE)
        im = im.filter(ImageFilter.DETAIL)
        return im
