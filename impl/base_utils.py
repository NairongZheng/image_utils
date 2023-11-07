import numpy as np


class BaseUtils:
    def __init__(self):
        pass

    def read_image(self):
        raise NotImplementedError

    def truncation(self, data: np.array):
        
        pass

    def run(self):
        raise NotImplementedError
