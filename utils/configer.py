"""
author:damonzheng
func:这是一个很丑陋的config, 但是没人会看, hhh
date:20231228
"""
import os
import argparse
import yaml
import json
from pathlib import Path
from yacs.config import CfgNode as CN
from utils.utils import namespace2dict, dict2namespace
from utils.logger import logger


class DefaultSet:
    """
    没用到这玩意
    一般是深度学习配置参数用
    这个image_utils比较简单, 没必要
    """

    def __init__(self):
        self._C = self.set_default()

    def set_default(self):
        _C = CN()
        _C.image_type = None
        _C.task_type = None

        _C.task_0 = CN()
        _C.task_0.image_path = None
        _C.task_0.save_path = None
        _C.task_0.rate = None

        _C.task_1 = CN()
        _C.task_1.image_path = None
        _C.task_1.save_path = None
        _C.task_1.size = None
        _C.task_1.stride = None
        _C.task_1.pad_zero = None

        _C.task_2 = CN()
        _C.task_2.image_path = None
        _C.task_2.save_path = None

        _C.task_3 = CN()
        _C.task_3.image_path = None
        _C.task_3.save_path = None
        _C.task_3.extra = CN(new_allowed=True)

        _C.task_4 = CN()
        _C.task_4.image_path = None
        _C.task_4.save_path = None
        _C.task_4.extra = CN(new_allowed=True)

        _C.task_5 = CN()
        _C.task_5.true_label_path = None
        _C.task_5.pre_label_path = None

        _C.task_6 = CN()
        _C.task_6.image_path = None
        _C.task_6.label_path = None
        _C.task_6.save_path = None
        _C.task_6.rate = None

        return _C

    def update_config(self, cfg, args):
        cfg.defrost()
        cfg.merge_from_file(args.cfg)  # 这里把yaml文件里的配置对defaults.py进行覆盖
        # cfg.merge_from_list(args.opts)
        cfg.freeze()


class ArgsParser:
    def __init__(self):
        # 默认配置参数
        # self.default_set = DefaultSet()
        # self.default_para = self.default_set._C
        self.args = self.parse_args()

    def parse_args(self):
        cur_file_path = Path(__file__).absolute()
        parser = argparse.ArgumentParser(description="too lazy to name")
        parser.add_argument(
            "--cfg",
            help="the path of config.yaml",
            default=os.path.join(cur_file_path.parent.parent, "config.yaml"),
        )
        args = parser.parse_args()
        with open(args.cfg, "r") as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)
        config_namespace = dict2namespace(config_dict)
        return config_namespace


class Config:
    def __init__(self):
        self.yaml_args = ArgsParser().args
        self.get_task_para()

    def check_task(self, task_type):
        self.idx_task_dict = {
            0: "对图像进行截断",
            1: "切图",
        }
        logger.info(
            f"supported task dict:\n{json.dumps(self.idx_task_dict, indent=4, ensure_ascii=False)}"
        )
        if task_type not in self.idx_task_dict:
            min_ = min(self.idx_task_dict.keys())
            max_ = max(self.idx_task_dict.keys())
            raise Exception(f"task type only support from {min_} to {max_}")

    def get_task_para(self):
        image_type = self.yaml_args.image_type
        task_type = self.yaml_args.task_type
        try:
            self.check_task(task_type)
        except Exception as e:
            logger.exception(e)
            quit()
        self.para = getattr(self.yaml_args, f"task_{task_type}")
        setattr(self.para, "image_type", image_type)
        setattr(self.para, "task_type", task_type)
        if "label_mapping" in self.para:
            label_mapping = self.para.label_mapping
            label_mapping = namespace2dict(label_mapping)
            self.para.label_mapping = label_mapping
        logger.info(f"当前任务是:{task_type}-{self.idx_task_dict[task_type]}")
        logger.info(
            f"参数设置是:\n{json.dumps(namespace2dict(self.para), indent=4, ensure_ascii=False)}"
        )


conf = Config().para
