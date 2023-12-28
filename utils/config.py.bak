"""
author:damonzheng
func:参数设置
date:20231107
"""


class Variables:
    def __init__(self):
        self.label_mapping = {
            "water": [0, 0, 255],
            "baresoil": [139, 0, 0],
            "road": [83, 134, 139],
            "industry": [255, 0, 0],
            "vegetation": [0, 255, 0],
            "residential": [205, 173, 0],
            "plantingarea": [139, 105, 20],
            "other": [178, 34, 34],
            "farms": [0, 139, 139],
        }


class Config:
    def __init__(self):
        """
        image_type: 本次处理的图像类型, 只有rgb(光学图/SAR图/label)跟hyper(高光谱/多光谱)可选
        task_type: 本次要对图像进行什么处理, 有以下可选:
            0: 对图像做截断拉伸, 常用于GF3的SAR图像(PIE处理之后)的第一步处理
            1: 切图
            2: 拼图
            3: 三通道转单通道
            4: 单通道转三通道
            5: 计算iou等语义分割评价指标
            6: 标签贴到图像
        """
        self.image_type: str = "rgb"  # 可选rgb/hyper
        self.task_type: int = 1
        self.vars: Variables = self.reset()

        pass

    def get_task_0_para(self):
        """
        image_path: 图片读取路径
        save_path: 图片保存路径
        rate: 截断拉伸的倍数(一般2.5或者3都ok)
        """
        para_dict = {
            "image_path": r"",
            "save_path": r"",
            "rate": 3,
        }
        return para_dict

    def get_task_1_para(self):
        para_dict = {
            "image_path": r"",
            "save_path": r"",
            "size": 512,
            "stride": 256,
            "pad_zero": False,
        }
        return para_dict

    def get_task_2_para(self):
        para_dict = {
            "image_path": r"",
            "save_path": r"",
        }
        return para_dict

    def get_task_3_para(self):
        para_dict = {
            "image_path": r"",
            "save_path": r"",
            "label_mapping": self.vars.label_mapping,
        }
        return para_dict

    def get_task_4_para(self):
        para_dict = {
            "image_path": r"",
            "save_path": r"",
            "label_mapping": self.vars.label_mapping,
        }
        return para_dict

    def get_task_5_para(self):
        """
        true_label_path: 真值标签的路径
        pre_label_path: 预测结果的路径
        """
        para_dict = {
            "true_label_path": r"",
            "pre_label_path": r"",
        }
        return para_dict

    def get_task_6_para(self):
        """
        image_path: 图像路径
        label_path: 标签路径

        """
        para_dict = {
            "image_path": r"",
            "label_path": r"",
            "save_path": r"",
            "rate": 0.3,
        }
        return para_dict

    def reset(self):
        """
        获取本次任务需要用到的参数
        通过Variables对象传出
        并进行打印
        """
        self.id_task_dict = {
            0: "对图像进行截断",
            1: "切图",
        }
        vars = Variables()
        self.check_task(self.task_type)
        self._get_para(self.task_type, vars)
        return vars

    def check_task(self, task_type):
        if task_type not in self.id_task_dict:
            min_ = min(self.id_task_dict.keys())
            max_ = max(self.id_task_dict.keys())
            raise Exception(f"task type only support from {min_} to {max_}")
            # assert (
            #     task_type >= min_ and task_type <= max_
            # ), f"task type only support from {min_} to {max_}"

    def _get_para(self, task_type: int, vars: Variables):
        """
        根据不同的task_type读取不同的参数
        并存放到Variables
        """
        get_para_func = getattr(self, f"get_task_{task_type}_para")
        self.para_dicit: dict = get_para_func()
        for key, val in self.para_dicit.items():
            setattr(vars, key, val)


conf = Config()
