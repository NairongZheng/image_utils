import numpy as np
import os
import copy
import json
import math
from tqdm import tqdm
from typing import List, Dict
from config import Config


class BaseUtils:
    def __init__(self):
        pass

    def read_path(self, path: str):
        """
        返回当前路径中所有文件的名字
        """
        # return [os.path.join(path, i) for i in os.listdir(path)]
        return os.listdir(path)

    def read_image(self):
        raise NotImplementedError

    def save_image(self):
        raise NotImplementedError

    def pad_image(self, raw_img_shape, small_img_size, strides, pad_zero):
        """
        根据原图尺寸、小图尺寸、步长、是否padding
        返回处理后可以切的行数、列数、padding后/裁剪后的大图尺寸
        """
        h, w, c = raw_img_shape
        row = math.floor((h - small_img_size) / strides) + 1
        col = math.floor((w - small_img_size) / strides) + 1
        row = row + 1 if pad_zero else row
        col = col + 1 if pad_zero else col
        pad_img = np.zeros(
            (
                (row - 1) * strides + small_img_size,
                (col - 1) * strides + small_img_size,
                c,
            )
        )
        return row, col, pad_img

    def cut_image(
        self,
        idx: int,
        pad_img,
        img_ext: str,
        row: int,
        col: int,
        size: int,
        stride: int,
    ):
        """
        切图
        参数: 大图编号、大图矩阵、图片格式、行数、列数、小图尺寸、步长
        返回: 字典, key为小图保存的名字、value为小图矩阵
        """
        cut_res_dict = {}  # key: img_name, value:img_array

        row_idx = 1
        for i in tqdm(range(row), total=row):
            row_start = i * stride
            row_end = i * stride + size
            col_idx = 1
            for j in range(col):
                col_start = j * stride
                col_end = j * stride + size
                small_pic = pad_img[row_start:row_end, col_start:col_end, :]
                small_name = (
                    "image"
                    + str(idx + 1).rjust(3, "0")
                    + "_"
                    + str(row_idx).rjust(3, "0")
                    + "row_"
                    + str(col_idx).rjust(3, "0")
                    + "col"
                    + img_ext
                )
                cut_res_dict[small_name] = small_pic
                col_idx += 1
            row_idx += 1
        return cut_res_dict

    def truncation(self, img, rate: float):
        """
        将img中大于rate倍均值的全部截断为`rate*mean`
        """
        img_mean = np.mean(img)
        img_new = copy.deepcopy(img)
        img_new[img > (rate * img_mean + 1e-7)] = rate * img_mean
        img_new = (img_new / np.max(img_new) + 1e-7) * 255.0
        return img_new

    def run(self):
        raise NotImplementedError

    def print(self, conf: Config):
        print_para = json.dumps(conf.para_dicit, indent=4)
        print("*" * 50)
        print(f"当前任务是:{conf.id_task_dict[conf.task_type]}\n参数设置是:\n{print_para}")
        print("*" * 50)
