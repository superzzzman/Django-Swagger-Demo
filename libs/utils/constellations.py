# coding: utf-8
import datetime


def get_constellation_by_datetime(dt: datetime.datetime) -> str:
    """获取星座

    :param dt: datetime.datetime: 日期
    :return: str
    """
    dates = (20, 19, 21, 20, 21, 22, 23, 23, 23, 24, 23, 22)
    constellations = ("摩羯座", "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座")
    if dt.day < dates[dt.month - 1]:
        return constellations[dt.month - 1]
    else:
        return constellations[dt.month]


def get_constellations_info() -> dict:
    constellation_dict: dict = {
        "3.21-4.19": "白羊座",
        "4.20-5.20": "金牛座",
        "5.21-6.21": "双子座",
        "6.22-7-22": "巨蟹座",
        "7.23-8.22": "狮子座",
        "8.23-9.22": "处女座",
        "9.23-10.23": "天秤座",
        "10.24-11.22": "天蝎座",
        "11.23-12.21": "射手座",
        "12.22-1.19": "摩羯座",
        "1.20-2.18": "水瓶座",
        "2.19-3.20": "双鱼座"
    }
    return constellation_dict
