"""
author:damonzheng
func:image utils
date:20231107
"""
from utils.configer import conf
from impl.rgb_utils import RGBUtils
if conf.image_type == "hyper":
    from impl.hyper_utils import HyperUtils


class MyClass:
    def __init__(self):
        self.conf = conf
        self.rgb_func = RGBUtils(self.conf)
        if self.conf.image_type == "hyper":
            self.hyper_func = HyperUtils(self.conf)

    def run(self):
        if self.conf.image_type == "rgb":
            self.rgb_func.run()
        elif self.conf.image_type == "hyper":
            self.hyper_func.run()


def main():
    main_func = MyClass()
    main_func.run()


if __name__ == "__main__":
    main()
