"""
author:damonzheng
func:hyper处理工具类
date:20231217
"""
import os
import numpy as np
import json
import gdal
import osr
from utils.configer import Config
from impl.base_utils import BaseUtils
from utils.logger import logger


class HyperUtils(BaseUtils):
    def __init__(self, conf: Config):
        super(HyperUtils, self).__init__()
        self.conf = conf

    def read_image(self, img_path: str):
        img = gdal.Open(img_path)
        height = img.RasterYSize  # 获取图像的行数
        width = img.RasterXSize  # 获取图像的列数
        band_num = img.RasterCount  # 获取图像波段数

        geo = img.GetGeoTransform()  # 仿射矩阵
        proj = img.GetProjection()  # 地图投影信息，字符串表示

        return img, height, width, band_num, geo, proj

    def hyper2numpy(self, dataset, h, w, band_num):
        """
        把gdal读出来的hyper的dataset格式转成矩阵形式
        """
        all_band_data = np.zeros((h, w, band_num))
        for i in range(0, band_num):
            all_band_data[:, :, i] = dataset.GetRasterBand(i + 1).ReadAsArray(
                0, 0, w, h
            )
        return all_band_data

    def numpy2hyper_save(self, array, h, w, save_path, geo=None, proj=None):
        """
        把多通道numpy保存成hyper
        """
        out_band_data = []
        band_num = array.shape[2]
        for i in range(band_num):
            out_band_data.append(array[:, :, i])
        del array
        driver = gdal.GetDriverByName("GTiff")  # 创建文件驱动
        dataset = driver.Create(save_path, w, h, band_num, 1)
        dataset.SetGeoTransform(geo)  # 写入仿射变换参数
        dataset.SetProjection(proj)  # 写入投影
        for i in range(band_num):
            dataset.GetRasterBand(i + 1).WriteArray(out_band_data[i])
        return

    def change_lonlat_dms(self, lonlat):
        """
        把经纬度转成用度、分、秒表示
        返回的是经纬度字符串
        """
        lon = lonlat[0]
        lat = lonlat[1]

        lon_degree = int(lon)
        lon_minute = int((lon - lon_degree) * 60)
        lon_second = ((lon - lon_degree) * 60 - lon_minute) * 60

        lat_degree = int(lat)
        lat_minute = int((lat - lat_degree) * 60)
        lat_second = ((lat - lat_degree) * 60 - lat_minute) * 60

        lon_str = "{}°{}'{:.2f}\"".format(lon_degree, lon_minute, lon_second)
        lat_str = "{}°{}'{:.2f}\"".format(lat_degree, lat_minute, lat_second)
        lonlat_str = str("(") + lon_str + str(", ") + lat_str + str(")")
        return lonlat_str

    def get_reference_sys(self, dataset):
        """
        获得该图的投影参考系和地理参考系
        """
        proj_rs = osr.SpatialReference()
        proj_rs.ImportFromWkt(dataset.GetProjection())
        geosr_s = proj_rs.CloneGeogCS()
        return proj_rs, geosr_s

    def geo2lonlat(self, dataset, point):
        """
        地理坐标转化成经纬度
        point是一个元组，存放的是地理坐标(x, y)
        返回的也是一个元组，就是该地理坐标转换之后的经纬度
        """
        x = point[0]
        y = point[1]
        proj_rs, geo_rs = self.get_reference_sys(dataset)
        ct = osr.CoordinateTransformation(proj_rs, geo_rs)
        coords = ct.TransformPoint(x, y)
        return coords[:2]

    def imagexy2geo(self, geo, row_col):
        """
        根据仿射矩阵geo计算图像某点的地理坐标
        row_col是一个元组，存放的是待计算的点与原点的偏移量
        返回的也是一个元组，就是该点的地理坐标(x, y)
        """
        row = row_col[0]
        col = row_col[1]
        px = geo[0] + col * geo[1] + row * geo[2]
        py = geo[3] + col * geo[4] + row * geo[5]
        return (px, py)

    def get_geo_and_proj(self, idx, pad_img, img_ext, row, col, size, stride):
        """
        切图时给计算小图设置geo个proj
        """
        img_geo_proj_dict = {}
        row_idx = 1
        for i in range(row):
            row_start = i * stride
            col_idx = 1
            for j in range(col):
                col_start = j * stride
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
                img_geo_proj_dict[small_name] = (row_start, col_start)
                col_idx += 1
            row_idx += 1
        return img_geo_proj_dict

    def run_task_7_func(self):
        """
        任务7: 读取高光谱并获得经纬度等信息
        """
        all_image_name = self.read_path(self.conf.image_path)
        info = {}
        for i, img_name in all_image_name:
            img_path = os.path.join(self.conf.image_path, img_name)
            img, height, width, band_num, geo, proj = self.read_image(img_path)
            # 计算图像四个点的地理坐标
            left_up = (geo[0], geo[3])
            right_up = self.imagexy2geo(geo, (0, width))
            left_down = self.imagexy2geo(geo, (height, 0))
            right_down = self.imagexy2geo(geo, (height, width))
            # 计算图像四个点的经纬度
            left_up_lonlat = self.geo2lonlat(img, left_up)
            right_up_lonlat = self.geo2lonlat(img, right_up)
            left_down_lonlat = self.geo2lonlat(img, left_down)
            right_down_lonlat = self.geo2lonlat(img, right_down)
            # 用度分秒表示图像四个点的经纬度
            left_up_lonlat_ = self.change_lonlat_dms(left_up_lonlat)
            right_up_lonlat_ = self.change_lonlat_dms(right_up_lonlat)
            left_down_lonlat_ = self.change_lonlat_dms(left_down_lonlat)
            right_down_lonlat_ = self.change_lonlat_dms(right_down_lonlat)
            # 整理获得的信息
            info[img_path] = {}
            info[img_path]["height"] = height
            info[img_path]["width"] = width
            info[img_path]["band_num"] = band_num
            info[img_path]["仿射矩阵"] = geo
            info[img_path]["投影"] = proj
            info[img_path]["左上角的经纬度"] = left_up_lonlat_
            info[img_path]["右上角的经纬度"] = right_up_lonlat_
            info[img_path]["左下角的经纬度"] = left_down_lonlat_
            info[img_path]["右下角的经纬度"] = right_down_lonlat_
        info = json.dumps(info, indent=4)
        logger.info("全部高光谱图片读取完成, 信息如下: ")
        logger.info(info)

    def run_task_8_func(self):
        all_image_name = self.read_path(self.conf.image_path)
        for i, img_name in all_image_name:
            img_path = os.path.join(self.conf.image_path, img_name)
            img, height, width, band_num, geo, proj = self.read_image(img_path)
            img = self.hyper2numpy(img, height, width, band_num)
            img = self.truncation(img, self.conf.rate)
            save_path = os.path.join(self.conf.save_path, img_name)
            self.numpy2hyper_save(img, height, width, save_path, geo, proj)
        return

    def run_task_9_func(self):
        all_image_name = self.read_path(self.conf.image_path)
        for i, img_name in all_image_name:
            img_ext = os.path.splitext(img_name)[1]
            img_path = os.path.join(self.conf.image_path, img_name)
            img, height, width, band_num, geo, proj = self.read_image(img_path)
            img = self.hyper2numpy(img, height, width, band_num)
            # 计算padding或者裁剪的尺寸
            row, col, pad_img = self.pad_image(
                img.shape,
                self.conf.size,
                self.conf.stride,
                self.conf.pad_zero,
            )
            # cut
            img_dict = self.cut_image(
                i,
                pad_img,
                img_ext,
                row,
                col,
                self.conf.size,
                self.conf.stride,
            )
            # 高光谱要多一步计算每张小图的仿射矩阵和投影信息
            img_geo_proj_dict = self.get_geo_and_proj(
                i,
                pad_img,
                img_ext,
                row,
                col,
                self.conf.size,
                self.conf.stride,
            )
            for small_img_name, small_img_arr in img_dict.items():
                save_path = os.path.join(self.conf.save_path, small_img_name)
                size = self.conf.size
                geo, proj = img_geo_proj_dict[small_img_name]
                self.numpy2hyper_save(small_img_arr, size, size, save_path, geo, proj)
        return

    def run_task_10_func(self):
        small_img_path = self.conf.image_path
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
            _, h, w, band_num, geo, proj = self.read_image(
                os.path.join(small_img_path, znr[i][0])
            )
            row = int(znr[i][small_pic_num_2 - 1].split("row_")[0].split("_")[1])
            col = int(znr[i][small_pic_num_2 - 1].split("row_")[1].split("col")[0])
            big_h = row * h
            big_w = col * w
            to_image = np.zeros((big_h, big_w, band_num), dtype=np.uint8)

            for y in range(0, row):
                row_start = y * h
                row_end = row_start + h
                for x in range(0, col):
                    col_start = x * w
                    col_end = col_start + w
                    small_pic, h, w, band_num, _, _ = self.read_image(
                        os.path.join(small_img_path, znr[i][k])
                    )
                    small_pic = self.hyper2numpy(small_pic, h, w, band_num)
                    k += 1
                    to_image[row_start:row_end, col_start:col_end, :] = small_pic
            save_img_name = "{}{}".format(i + 1, small_img_ext)
            save_path = os.path.join(self.conf.save_path, save_img_name)
            self.numpy2hyper_save(to_image, big_h, big_w, save_path, geo, proj)
        return

    def run(self):
        """
        run函数, 运行入口
        """
        run_task_func = getattr(self, f"run_task_{self.conf.task_type}_func")
        logger.info(f"{run_task_func.__name__} is running!")
        run_task_func()
