# 一个糊弄的README

## 支持功能
目前只支持以下功能, 别的可以去[链接](https://github.com/NairongZheng/utils)里翻...
```python
{
    # rgb(SAR/label)
    0: "对图像进行截断拉伸归一化",
    1: "切图",
    2: "拼图",
    3: "三通道标签转成单通道",
    4: "单通道标签转成三通道",
    5: "计算语义分割指标",
    6: "标签贴到原图上",
    # hyper
    7: "读取高光谱并获得经纬度等信息",
    8: "高光谱阶段拉伸(一般不用)",
    9: "高光谱切图",
    10: "高光谱拼图"
}
```
## 环境配置
1. 如果是在Windows跑（前后处理倒也方便, 推荐这个, 毕竟服务器看图也不方便），环境很好弄，不赘述。其中高光谱用到的gdal可以从[python whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/)下载。
2. 如果是在Linux跑，可以使用提供的Dockerfile，具体查看（懒得写）`./docker/Dockerfile`。
3. 注意gdal版本用的是2不是3！！
4. 如果需要使用Dockerfile配置环境的话，其中一些软件包可通过镜像下载较快：
   1. anaconda：[清华源](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)
   2.  miniconda：[清华源](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/)
   3.  gdal：[conda官方库](https://anaconda.org/conda-forge/gdal/files?page=2&version=2.4.4)

> 对环境配置感兴趣的可以看看[博客](https://blog.csdn.net/a264672/article/details/134770104)

## 使用
1. 建议路径为英文且不带空格。
2. 只需要在`./config.yaml`中设置好参数，运行`./main.py`即可。具体去看`./config.yaml`的注释，很简单，不赘述。
3. 使用有问题、有报错或者需要新加别的功能，可以发邮件 (damonzheng46@gmail.com) 联系。35岁之前还健在的话会回。