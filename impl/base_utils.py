"""
author:damonzheng
func:rgb_utils和hyper_utils的父类
date:20231108
"""
import os
import copy
import numpy as np
import json
import math
from tqdm import tqdm
from PIL import Image
import cv2
from typing import List, Dict
from utils.configer import Config
from impl import utils
from utils.logger import logger


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

    def truncation(self, img, rate: float):
        """
        将img中大于rate倍均值的全部截断为`rate*mean`
        """
        img_mean = np.mean(img)
        img_new = copy.deepcopy(img)
        img_new[img > (rate * img_mean + 1e-7)] = rate * img_mean
        img_new = (img_new / np.max(img_new) + 1e-7) * 255.0
        return img_new

    def pad_image(self, raw_img, small_img_size, strides, pad_zero):
        """
        根据原图尺寸、小图尺寸、步长、是否padding
        返回处理后可以切的行数、列数、padding后/裁剪后的大图
        """
        h, w, c = raw_img.shape
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
        pad_h, pad_w, pad_c = pad_img.shape
        if pad_zero:
            pad_img[:h, :w, :c] = raw_img
        else:
            pad_img = raw_img[:pad_h, :pad_w, :pad_c]
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
        for i in range(row):
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

    def connect_image(self, small_img_path):
        """
        拼图
        """
        pass

    def change_label_3to1(self, label, label_mapping: Dict):
        """
        三转成单通道
        """
        temp = label.copy()
        label_mask = np.zeros((label.shape[0], label.shape[1]))
        for i, (num_cls, rgb) in enumerate(label_mapping.items()):
            num, cls = num_cls.split("_")
            label_mask[
                (
                    ((temp[:, :, 0] == rgb[0]) & (temp[:, :, 1] == rgb[1]))
                    & (temp[:, :, 2] == rgb[2])
                )
            ] = int(num)

        return label_mask

    def change_label_1to3(self, label, label_mapping: Dict):
        """
        单通道转三通道
        """
        height, width, c = label.shape
        if c != 1:
            raise Exception(f"the input images must be 1 channel, but your images' channel is {c}")
        label = np.reshape(label, (height, width))
        new_label = np.zeros([height, width, 3])
        for i, (k, v) in enumerate(label_mapping.items()):
            globals()[k] = label == i
        for i, (k, v) in enumerate(label_mapping.items()):
            new_label[:, :, 0] += globals()[k] * v[0]
            new_label[:, :, 1] += globals()[k] * v[1]
            new_label[:, :, 2] += globals()[k] * v[2]
        return new_label

    def cal_indicators(self, true_pre_list: List[Dict], label_mapping):
        """
        语义分割计算一些指标, 包括confusion_matrix_all, iou, miou, fwiou, kappa, acc
        """
        num_class = len(label_mapping)
        confusion_matrix_all = np.zeros((num_class, num_class))
        for i in range(len(true_pre_list)):
            true_pre_dict = true_pre_list[i]
            true_lab_arr = copy.deepcopy(true_pre_dict["true_lab_arr"])
            pre_lab_arr = copy.deepcopy(true_pre_dict["pre_lab_arr"])
            if true_lab_arr.shape[2] == 1:
                true_lab_arr = np.squeeze(true_lab_arr, axis=2)
            elif true_lab_arr.shape[2] == 3:
                true_lab_arr = self.change_label_3to1(true_lab_arr, label_mapping)
            if pre_lab_arr.shape[2] == 1:
                pre_lab_arr = np.squeeze(pre_lab_arr, axis=2)
            elif pre_lab_arr.shape[2] == 3:
                pre_lab_arr = self.change_label_3to1(pre_lab_arr, label_mapping)

            confusion_matrix = utils._generate_matrix(
                true_lab_arr.astype(np.int8),
                pre_lab_arr.astype(np.int8),
                num_class=len(label_mapping),
            )
            confusion_matrix_all = confusion_matrix_all + confusion_matrix
            # miou = _Class_IOU(confusion_matrix_all)
            (miou, iou) = utils.meanIntersectionOverUnion(confusion_matrix_all)
            fwiou = utils.Frequency_Weighted_Intersection_over_Union(
                confusion_matrix_all
            )
            kappa = utils.Kappa(confusion_matrix_all)
        acc = np.diag(confusion_matrix_all).sum() / confusion_matrix_all.sum()
        result_dict = {
            "confusion_matrix_all": confusion_matrix_all.tolist(),
            "iou": iou.tolist(),
            "miou": miou,
            "fwiou": fwiou,
            "kappa": kappa,
            "acc": acc,
        }
        result_dict = json.dumps(result_dict, indent=4)
        return result_dict

    def image_with_mask(self, image_path, label_path, save_path, rate):
        # image = cv2.imread(image_path)

        # 图像太大的画，cv2没办法打开，就用PIL
        image = Image.open(image_path)
        image = np.asarray(image)
        image = image[:, :, ::-1]
        label = cv2.imread(label_path)
        combine = cv2.addWeighted(image, 1 - rate, label, rate, 0)
        cv2.imwrite(save_path, combine)
        pass

    def run(self):
        raise NotImplementedError
