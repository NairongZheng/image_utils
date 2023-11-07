"""
author:damonzheng
func:参数设置
date:20231107
"""


class Variables:
    def __init__(self):
        pass


class Config:
    def __init__(self):
        """
        image_type: 本次处理的图像类型, 只有rgb(光学图/SAR图/label)跟hyper(高光谱/多光谱)可选
        task_type: 本次要对图像进行什么处理, 有以下可选:
            0: 对图像做截断拉伸, 常用于GF3的SAR图像(PIE处理之后)的第一步处理
        """
        self.image_type: str = "rgb"  # 可选rgb/hyper
        self.task_type: int = 0
        self.vars: Variables = self.reset()

        pass

    def get_mode_0_para(self):
        """
        image_path: 图片读取路径
        save_path: 图片保存路径
        rate: 截断拉伸的倍数(一般2.5或者3都ok)
        """
        para_dict = {
            "image_path": r"D:\code_python\utils\image_utils\example\sar_images",
            "save_path": r"D:\code_python\utils\image_utils\example\labels",
            "rate": 3,
        }
        return para_dict

    def reset(self):
        """
        获取本次任务需要用到的参数
        并通过Variables对象传出
        """
        vars = Variables()
        self._get_para(self.task_type, vars)
        return vars

    def _get_para(self, task_type: int, vars: Variables):
        """
        根据不同的task_type读取不同的参数
        并存放到Variables
        """
        get_para_func = getattr(self, f"get_mode_{task_type}_para")
        para_dicit: dict = get_para_func()
        for key, val in para_dicit.items():
            setattr(vars, key, val)


conf = Config()
