from PIL import Image
import numpy as np
import os
import copy
from tqdm import tqdm
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
        return

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

            for small_img_name, small_img_arr in img_dict.items():
                self.save_image(small_img_arr, small_img_name)
        return

    def run_task_2_func(self):
        """
        任务2: 拼图
        """
        small_img_path = self.conf.vars.image_path
        img_name = os.listdir(small_img_path)
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
            h, w, c = Image.open(os.path.join(small_img_path, znr[i][0])).size
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
        return

    def run_task_3_func(self):
        """
        任务3: 标签三通道转单通道
        """
        all_label_names = os.listdir(self.conf.vars.image_path)
        for label_name in all_label_names:
            lab = self.read_image(os.path.join(self.conf.vars.image_path, label_name))
            lab = self.change_label_3to1(
                lab, copy.deepcopy(self.conf.vars.label_mapping)
            )
            self.save_image(lab, os.path.join(self.conf.vars.save_path, label_name))
        return

    def run_task_4_func(self):
        """
        任务4: 标签单通道转三通道
        """
        all_label_names = os.listdir(self.conf.vars.image_path)
        for label_name in all_label_names:
            lab = self.read_image(os.path.join(self.conf.vars.image_path, label_name))
            lab = self.change_label_1to3(
                lab, copy.deepcopy(self.conf.vars.label_mapping)
            )
            self.save_image(lab, os.path.join(self.conf.vars.save_path, label_name))
        return

    def run_task_5_func(self):
        true_pre_list = []
        true_lab_names = os.listdir(self.conf.vars.true_label_path).sort()
        pre_lab_names = os.listdir(self.conf.vars.pre_label_path).sort()
        for i in range(len(true_lab_names)):
            true_lab_arr = self.read_image(
                os.path.join(self.conf.vars.true_label_path, true_lab_names[i])
            )
            pre_lab_arr = self.read_image(
                os.path.join(self.conf.vars.pre_label_path, pre_lab_names[i])
            )
            true_pre_list.append(
                {"true_lab_arr": true_lab_arr, "pre_lab_arr": pre_lab_arr}
            )
        self.cal_indicators(true_pre_list, self.conf.vars.label_mapping)
        return

    def run(self):
        """
        run函数, 运行入口
        """
        run_task_func = getattr(self, f"run_task_{self.conf.task_type}_func")
        run_task_func()
