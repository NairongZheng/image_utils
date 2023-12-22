# 一个糊弄的README
## 环境配置
1. 如果是在Windows跑（前后处理倒也方便），环境很好弄，不赘述。其中gdal可以从[python whl](https://www.lfd.uci.edu/~gohlke/pythonlibs/)下载。
2. 如果是在Linux跑，可以使用提供的Dockerfile，具体查看（懒得写）`./docker/Dockerfile`。
3. 注意gdal版本用的是2不是3！！
4. 如果需要使用Dockerfile配置环境的话，其中一些软件包可通过镜像下载较快：
   1. anaconda：[清华源](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)
   2.  miniconda：[清华源](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/)
   3.  gdal：[conda官方库](https://anaconda.org/conda-forge/gdal/files?page=2&version=2.4.4)

> 对环境配置感兴趣的可以看看[博客](https://blog.csdn.net/a264672/article/details/134770104)

## 使用
只需要在`./config.py`的Config类中设置好参数，运行`./main.py`即可。具体去看Config类初始化的注释，很简单，不赘述。