# -*- coding: UTF-8 -*-

import datetime
import numpy as np


def to_date_object(date):
    """
    转换字符串或日期时间对象为日期对象（直接忽略时分秒部分）
    :param date:
    :return:
    """
    if date is None:
        return None

    if isinstance(date, datetime.datetime):
        return date.date()

    if isinstance(date, datetime.date):
        return date

    date = to_time_object(date)
    date = date.date()

    return date


def to_time_object(dt):
    """
    转换字符串或日期时间对象为时间对象
    :param dt:
    :return:
    """
    if dt is None:
        return None

    adjust_time_zone = False

    if isinstance(dt, str):
        n = len(dt)
        if 8 == n:
            fmt = '%Y%m%d'
        elif 10 == n:
            pos = dt.find('/')
            if -1 == pos:
                fmt = '%Y-%m-%d' if 4 == dt.find('-') else '%m-%d-%Y'
            elif 4 == pos:
                fmt = '%Y/%m/%d'
            else:
                fmt = '%m/%d/%Y'
        elif n > 4 and dt[n - 4:] == ' GMT':
            fmt = '%a, %d %b %Y %H:%M:%S GMT'
            adjust_time_zone = True  # 需要调整时区，一般 HTTP 请求头里用 GMT 时间表示
        else:
            fmt = '%Y-%m-%d %H:%M:%S'
        dt = datetime.datetime.strptime(dt, fmt)

        # 需要调整时区
        if adjust_time_zone:
            dt = dt + datetime.timedelta(seconds=-datetime.time.timezone)
    elif isinstance(dt, np.datetime64):
        dt = datetime.datetime.fromtimestamp(dt.astype('O') / 1e9)
    elif isinstance(dt, datetime.datetime):
        pass
    elif isinstance(dt, datetime.date):
        dt = datetime.datetime(dt.year, dt.month, dt.day)
    else:
        raise TypeError('date type error! ' + str(type(dt)))

    return dt


def to_date_str_fmt(date, fmt):
    """
    转换为日期字符串
    :param date:
    :param fmt:
    :return:
    """
    if date is None:
        return ""

    date = to_date_object(date)
    return date.strftime(fmt)


def to_date_str(date):
    """转换为日期字符串 %Y-%m-%d
    :param date:
    :return:
    """
    return to_date_str_fmt(date, '%Y-%m-%d')


def to_date_str_short(date):
    """转换为日期字符串 %Y%m%d
    :param date:
    :return:
    """
    return to_date_str_fmt(date, '%Y%m%d')


def to_datetime_str_fmt(dt, fmt):
    """
    转换为日期时间字符串
    :param dt:
    :param fmt:
    :return:
    """
    if dt is None:
        return ""

    dt = to_time_object(dt)
    return dt.strftime(fmt)


def to_datetime_str(dt):
    """转换为日期字符串 %Y-%m-%d %H:%M:%S
    :param dt:
    :return:
    """
    return to_datetime_str_fmt(dt, '%Y-%m-%d %H:%M:%S')
