from PIL import Image
import numpy as np
import os
import copy
from config import Config
from impl.base_utils import BaseUtils


class RGBUtils(BaseUtils):
    def __init__(self, conf: Config):
        super(RGBUtils, self).__init__()
        self.conf = conf

    def read_image(self, img_path: str):
        """
        读取图片
        """
        img = Image.open(img_path)
        img = np.asarray(img)
        if len(img.shape) < 3:
            img = np.expand_dims(copy.deepcopy(img), axis=1)
        return img

    def save_image(self, img, img_path: str):
        """
        保存图片
        """
        img = Image.fromarray(np.uint8(img))
        save_path = os.path.join(self.conf.vars.save_path, img_path)
        img.save(save_path)

    def run_task_0_func(self):
        """
        任务0: 将图像截断拉伸
        """
        all_image_name = self.read_path(self.conf.vars.image_path)
        for i, img_name in all_image_name:
            img_path = os.path.join(self.conf.vars.image_path, img_name)
            img = self.read_image(img_path)
            img = self.truncation(img, self.conf.vars.rate)
            self.save_image(img, img_name)

    def run_task_1_func(self):
        """
        任务1: 切图
        """
        all_image_name = self.read_path(self.conf.vars.image_path)
        for i, img_name in all_image_name:
            img_ext = os.path.splitext(img_name)[1]
            img_path = os.path.join(self.conf.vars.image_path, img_name)
            img = self.read_image(img_path)
            row, col, pad_img = self.pad_image(
                img.shape,
                self.conf.vars.size,
                self.conf.vars.stride,
                self.conf.vars.pad_zero,
            )
            img_dict = self.cut_image(
                i,
                pad_img,
                img_ext,
                row,
                col,
                self.conf.vars.size,
                self.conf.vars.stride,
            )

    def run(self):
        """
        run函数, 运行入口
        """
        run_task_func = getattr(self, f"run_task_{self.conf.task_type}_func")
        run_task_func()
