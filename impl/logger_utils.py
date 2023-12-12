import logging
import time
import os


class Logger:
    def __init__(self):
        self.reset()

    def reset(self):
        pwd = os.path.dirname(os.path.abspath(__file__))
        proj_path = os.path.dirname(pwd)
        log_path = os.path.join(proj_path, "log")
        self.create_logger(log_path)

    def create_logger(self, log_path):
        time_str = time.strftime("%Y-%m-%d-%H-%M")
        head = "%(asctime)-15s %(message)s"
        logger_path = os.path.join(log_path, f"{time_str}.log")
        logging.basicConfig(filename=logger_path, format=head)
        # logger = logging.FileHandler(filename=logger_path, encoding='utf-8')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        console = logging.StreamHandler()
        logging.getLogger("").addHandler(console)
        return
