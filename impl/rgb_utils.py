from PIL import Image
import numpy as np
from config import Config
from impl.base_utils import BaseUtils


class RGBUtils(BaseUtils):
    def __init__(self, conf: Config):
        super(RGBUtils, self).__init__()
        self.conf = conf

    def read_image(self, img_path):
        img = Image.open(img_path)
        img = np.asarray(img)
        return img

    def run(self):
        if self.conf.task_type == 0:
            data = self.read_image(img_path=self.conf.vars.image_path)
            self.truncation(data)
        pass
