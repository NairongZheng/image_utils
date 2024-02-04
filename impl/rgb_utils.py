"""
author:damonzheng
func:rgb处理工具类
date:20231108
"""
import os
import copy
from PIL import Image
import numpy as np
from tqdm import tqdm
from utils.configer import Config
from impl.base_utils import BaseUtils
from utils.logger import logger
# from utils.bar import show_bar

class RGBUtils(BaseUtils):
    """
    处理rgb图像(sar也当作是)
    """
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
            img = np.expand_dims(copy.deepcopy(img), axis=2)
        return img

    def save_image(self, img, img_path: str):
        """
        保存图片
        """
        img = Image.fromarray(np.uint8(img))
        save_path = os.path.join(self.conf.save_path, img_path)
        img.save(save_path)

    # @show_bar
    def run_task_0_func(self):
        """
        任务0: 将图像截断拉伸, 一般只有SAR图像, 如高分三地理信息编码之后想转成"普通图像"用的
        """
        all_image_name = self.read_path(self.conf.image_path)
        for img_name in tqdm(all_image_name, total=len(all_image_name)):
            img_path = os.path.join(self.conf.image_path, img_name)
            img = self.read_image(img_path)
            img = self.truncation(img, self.conf.rate)
            self.save_image(img, img_name)
        return {"bar_len": len(all_image_name)} # 为了配合装饰器显示进度条

    # @show_bar
    def run_task_1_func(self):
        """
        任务1: 切图
        """
        all_image_name = self.read_path(self.conf.image_path)
        for i, img_name in tqdm(enumerate(all_image_name), total=len(all_image_name)):
            img_ext = os.path.splitext(img_name)[1]
            img_path = os.path.join(self.conf.image_path, img_name)
            img = self.read_image(img_path)
            row, col, pad_img = self.pad_image(
                img,
                self.conf.size,
                self.conf.stride,
                self.conf.pad_zero,
            )
            img_dict = self.cut_image(
                i,
                pad_img,
                img_ext,
                row,
                col,
                self.conf.size,
                self.conf.stride,
            )

            for small_img_name, small_img_arr in img_dict.items():
                self.save_image(small_img_arr, small_img_name)
        # return {"bar_len": len(all_image_name)} # 为了配合装饰器显示进度条

    # @show_bar
    def run_task_2_func(self):
        """
        任务2: 拼图
        """
        small_img_path = self.conf.image_path
        img_name = self.read_path(small_img_path)
        img_name.sort()
        small_img_ext = os.path.splitext(img_name[0])[1]

        small_pic_num = len(img_name)
        big_pic_num = int(img_name[small_pic_num - 1].split("image")[1].split("_")[0])

        # 创建一个列表。每个元素存放同一个大图切下来的所有小图名
        znr = [[] for i in range(0, big_pic_num)]
        for i in range(0, small_pic_num):
            znr[int(img_name[i].split("image")[1].split("_")[0]) - 1].append(
                img_name[i]
            )

        for i in range(0, big_pic_num):
            k = 0
            small_pic_num_2 = len(znr[i])
            h, w, c = np.array(Image.open(os.path.join(small_img_path, znr[i][0]))).shape
            row = int(znr[i][small_pic_num_2 - 1].split("row_")[0].split("_")[1])
            col = int(znr[i][small_pic_num_2 - 1].split("row_")[1].split("col")[0])
            to_image = np.zeros((row * h, col * w, c), dtype=np.uint8)

            for y in tqdm(range(0, row), total=row):
                row_start = y * h
                row_end = row_start + h
                for x in range(0, col):
                    col_start = x * w
                    col_end = col_start + w
                    small_pic = Image.open(os.path.join(small_img_path, znr[i][k]))
                    k += 1
                    to_image[row_start:row_end, col_start:col_end, :] = small_pic
            save_img_name = "{}{}".format(i + 1, small_img_ext)
            self.save_image(to_image, save_img_name)
        # return {"bar_len": len(img_name)} # 为了配合装饰器显示进度条

    def run_task_3_func(self):
        """
        任务3: 标签三通道转单通道
        """
        all_label_names = self.read_path(self.conf.image_path)
        for label_name in tqdm(all_label_names, total=len(all_label_names)):
            lab = self.read_image(os.path.join(self.conf.image_path, label_name))
            lab = self.change_label_3to1(
                lab, copy.deepcopy(self.conf.label_mapping)
            )
            self.save_image(lab, os.path.join(self.conf.save_path, label_name))
        return

    def run_task_4_func(self):
        """
        任务4: 标签单通道转三通道
        """
        all_label_names = self.read_path(self.conf.image_path)
        try:
            for label_name in tqdm(all_label_names, total=len(all_label_names)):
                lab = self.read_image(os.path.join(self.conf.image_path, label_name))
                lab = self.change_label_1to3(
                    lab, copy.deepcopy(self.conf.label_mapping)
                )
                self.save_image(lab, os.path.join(self.conf.save_path, label_name))
        except Exception as e:
            logger.exception(e)
            quit()
        return

    def run_task_5_func(self):
        """
        任务5: 语义分割计算一些指标, 包括confusion_matrix_all, iou, miou, fwiou, kappa, acc
        """
        true_pre_list = []
        try:
            true_lab_names = sorted(self.read_path(self.conf.true_label_path))
            pre_lab_names = sorted(self.read_path(self.conf.pre_label_path))
            if len(true_lab_names) != len(pre_lab_names):
                raise Exception(f"true_label_num:{len(true_lab_names)}, but pre_label_num:{len(pre_lab_names)}")
        except Exception as e:
            logger.exception(e)
            quit()
        
        for i in tqdm(range(len(true_lab_names)), total=len(true_lab_names)):
            true_lab_arr = self.read_image(
                os.path.join(self.conf.true_label_path, true_lab_names[i])
            )
            pre_lab_arr = self.read_image(
                os.path.join(self.conf.pre_label_path, pre_lab_names[i])
            )
            true_pre_list.append(
                {"true_lab_arr": true_lab_arr, "pre_lab_arr": pre_lab_arr}
            )
        result_dict = self.cal_indicators(true_pre_list, self.conf.label_mapping)
        logger.info(f"计算结果如下:\n{result_dict}")
        return

    def run_task_6_func(self):
        """
        任务6: 将标签贴到原图上, 方便比对
        """
        try:
            all_images = sorted(self.read_path(self.conf.image_path))
            all_labels = sorted(self.read_path(self.conf.label_path))
            rate = self.conf.rate
            if len(all_images) != len(all_labels):
                raise Exception(f"image_num:{len(all_images)}, but label_num:{len(all_labels)}")
            if rate < 0 or rate > 1:
                raise Exception(f"rate must be in [0, 1], but your rate is {rate}, 在这个范围外你把控不住")
        except Exception as e:
            logger.exception(e)
            quit()
        for i in tqdm(range(len(all_images)), total=len(all_labels)):
            img_name, img_ext = all_images[i].split(".")
            img_path = os.path.join(self.conf.image_path, all_images[i])
            lab_path = os.path.join(self.conf.label_path, all_labels[i])
            save_path = os.path.join(self.conf.save_path, img_name + ".jpg")
            self.image_with_mask(img_path, lab_path, save_path, rate)
        return

    def run(self):
        """
        run函数, 运行入口
        """
        run_task_func = getattr(self, f"run_task_{self.conf.task_type}_func")
        logger.info(f" ============== {run_task_func.__name__} is running ============== ")
        run_task_func()
        logger.info(f" ============== {run_task_func.__name__} finish ============== ")
