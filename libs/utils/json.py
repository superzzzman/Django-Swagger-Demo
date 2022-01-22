# coding: utf-8

import json
import logging

log = logging.getLogger(__name__)


def json_loads(json_data, default=dict):
    """json to python data type

    :param json_data: json: json串
    :param default: 无法序列化时返回值
    :return:
    """
    if json_data is None:
        return default()
    try:
        data = json.loads(json_data)
    except (json.JSONDecodeError, TypeError) as e:
        # raise e
        log.warning(e)
        log.warning(json_data)
        data = default()
    return data
