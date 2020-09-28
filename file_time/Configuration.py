from datetime import datetime
import time, datetime
import random


class Configuration:
    def __init__(self):
        self.start_day = None
        self.time_random_start = 0
        self.time_random_end = 0
        self.time_range = 0
        self.increment_day = 0
        self.offset_sec = 0
        self.root = ""
        # self.add_sec = 0

    def set_start_day(self, value):
        self.start_day = value

    def set_time_random_start(self, value):
        self.time_random_start = value

    def set_time_random_end(self, value):
        self.time_random_end = value

    def set_increment_day(self, value):
        self.increment_day = value

    def set_root(self, value):
        self.root = value

    def set_add_min(self, value):
        self.add_min = value

    def set_add_sec(self, value):
        self.add_sec = value

    """
    获取起始时间的秒级别
    """

    def get_start_day_mktime(self):
        start = time.strptime(self.start_day + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(start))

    """
    处理随机时刻的数据
    """

    def calculation_time_random_delta(self):
        start = time.strptime("1971-01-01 " + self.time_random_start, "%Y-%m-%d %H:%M:%S")
        const = time.strptime("1971-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        end = time.strptime("1971-01-01 " + self.time_random_end, "%Y-%m-%d %H:%M:%S")
        start_stamp = int(time.mktime(start))
        end_stamp = int(time.mktime(end))
        const_stamp = int(time.mktime(const))
        self.time_range = end_stamp - start_stamp
        self.offset_sec = start_stamp - const_stamp
        self.get_increment_day_mktime()

    """
    获取随机时间段里面的随机时间，起始时间+随机区间值
    """

    def get_random_delta(self):
        print(random.randint(0, self.time_range))
        return self.offset_sec + random.randint(0, self.time_range)

    """
    按照自增天数转换为秒
    """

    def get_increment_day_mktime(self):
        return int(self.increment_day) * 24 * 60 * 60
