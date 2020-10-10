from datetime import datetime
import time, datetime
import random


def standard_time():
    return time.localtime(Configuration.STANDARD_TIME)


class Configuration:
    STANDARD_TIME = time.mktime((1971, 1, 1, 0, 0, 0, 0, 0, 0))

    def __init__(self):
        self.start_day = None
        self.time_random_start = 0
        self.time_random_end = 0
        self.time_range = 0
        self.increment_day = 0
        self.offset_sec = 0
        self.root = ""

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

    def get_start_day(self):
        return self.start_day

    def get_time_random_start(self):
        return self.time_random_start

    def get_time_random_end(self):
        return self.time_random_end

    def get_increment_day(self):
        return self.increment_day

    def get_root(self):
        return self.root

    def calculation_time_random_delta(self):
        """
        处理随机时刻的数据
        :return:
        """
        self.time_range = self.get_time_random_end() - self.get_time_random_start()
        self.offset_sec = self.get_time_random_start() - Configuration.STANDARD_TIME

    def get_random_delta(self):
        """
        获取随机时间段里面的随机时间，起始时间+随机区间值
        """
        print(random.randint(0, self.time_range))
        return self.offset_sec + random.randint(0, self.time_range)

    def get_increment_day_mktime(self):
        """
        按照自增天数转换为秒
        """
        return int(self.increment_day) * 24 * 60 * 60
