import argparse
import yaml
import utils
import os
from pathlib import Path
from yacs.config import CfgNode as CN


class DefaultSet:
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
        self.default_set = DefaultSet()
        self.default_para = self.default_set._C
        self.parse_args()

    def parse_args(self):
        cur_file_path = Path(__file__).absolute()
        parser = argparse.ArgumentParser(description="too lazy to name")
        parser.add_argument(
            "--cfg", help="the path of config.yaml", default=os.path.join(cur_file_path.parent.parent, "config.yaml")
        )
        args = parser.parse_args()
        # # 其实这么加载就行, 省的麻烦
        # with open(args.cfg, "r") as f:
        #     config_yaml = yaml.load(f, Loader=yaml.FullLoader)
        self.default_set.update_config(self.default_para, args)


class Config:
    def __init__(self):
        self.argsparser = ArgsParser()
        task_type = self.argsparser.default_para.task_type
        para = getattr(self.argsparser.default_para, f"task_{task_type}")
        pass


conf = Config()
