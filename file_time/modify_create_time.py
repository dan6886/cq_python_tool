#!/usr/bin/env python

import os
from configparser import ConfigParser

from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time
import win32timezone
import configparser

from file_time.Configuration import Configuration

"""
该方法是从网上查来，借鉴一下没有调用
"""


def modifyFileTime(filePath, createTime, modifyTime, accessTime, offset):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    try:
        format = "%Y-%m-%d %H:%M:%S"  # 时间格式
        cTime_t = timeOffsetAndStruct(createTime, format, offset[0])
        mTime_t = timeOffsetAndStruct(modifyTime, format, offset[1])
        aTime_t = timeOffsetAndStruct(accessTime, format, offset[2])

        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)

        createTimes = Time(time.mktime(cTime_t))
        accessTimes = Time(time.mktime(aTime_t))
        modifyTimes = Time(time.mktime(mTime_t))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except:
        return 1


def timeOffsetAndStruct(times, format, offset):
    return time.localtime(time.mktime(time.strptime(times, format)) + offset)


config: ConfigParser = configparser.ConfigParser()
configuration = Configuration()

count = 0

"""
读取配置文件
"""


def read_config():
    config.read("config.ini", encoding="utf-8-sig")
    start_day = config.get("config", "start_day")
    configuration.set_start_day(start_day)

    time_random_start = config.get("config", "time_random_start")
    configuration.set_time_random_start(time_random_start)

    time_random_end = config.get("config", "time_random_end")
    configuration.set_time_random_end(time_random_end)

    add_day = config.get("config", "add_day")
    configuration.set_increment_day(add_day)

    root = config.get("config", "root")
    configuration.set_root(root)
    #
    # add_min = config.get("config", "add_min")
    # configuration.set_add_min(add_min)

    # add_second = config.get("config", "add_second",fallback=None)
    # configuration.set_add_sec(add_second)

    configuration.calculation_time_random_delta()


"""
遍历文件夹这里只遍历一层就退出
"""


def start_walk():
    global count
    all_files = None
    for root, dirs, files in os.walk(configuration.root):
        all_files = files
        break

    for file_name in all_files:
        file_name = configuration.root + file_name
        start_time = configuration.get_start_day_mktime()
        add_time = configuration.get_increment_day_mktime() * count
        rand_time = configuration.get_random_delta()
        result = int(start_time) + int(add_time) + int(rand_time)
        print(time.localtime(result))
        result_time = time.localtime(result)
        code = modifyFileAllTime(file_name, result_time)
        print(code)
        count = count + 1


def modifyFileAllTime(filePath, createTime):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    print(filePath, createTime)
    try:
        format = "%Y-%m-%d %H:%M:%S"  # 时间格式
        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)

        createTimes = Time(time.mktime(createTime))
        accessTimes = Time(time.mktime(createTime))
        modifyTimes = Time(time.mktime(createTime))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except Exception as e:
        print(e)
        return 1


if __name__ == '__main__':
    read_config()
    start_walk()
    input("点击回车键结束")

# 调用
# cTime = "2019-02-02 00:01:02"  # 创建时间
# mTime = "2019-02-02 00:01:03"  # 修改时间
# aTime = "2019-02-02 00:01:04"  # 访问时间
#
# fName = r"D:\g.log"  # 文件路径
# offset = (0, 1, 2)  # 偏移的秒数
# r = modifyFileTime(fName, cTime, mTime, aTime, offset)
# if r == 0: print('修改完成')
# if r == 1: print('修改失败')
