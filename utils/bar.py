"""
author:damonzheng
func:进度条装饰器, 但是是一个虚假的进度条.....以后再实现吧, 暂时用tqdm麻烦一点
date:20231108
"""
import functools
from tqdm import tqdm

def show_bar(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if 'bar_len' in result:
            bar_len = result['bar_len']
        else:
            bar_len = 100  # 默认进度条长度为100

        with tqdm(total=bar_len, desc='Processing') as pbar:
            pbar.update(bar_len - pbar.n)

        return result

    return wrapper