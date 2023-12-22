FROM ubuntu:20.04
LABEL maintainer="damonzheng46@gmail.com" date="20231221"
SHELL ["/bin/bash","-c"]
COPY linux-64_gdal-2.4.4-py38hfe926b7_1.tar.bz2 /tmp
COPY Anaconda3-2023.09-0-Linux-x86_64.sh /tmp
# COPY Miniconda3-py310_23.5.1-0-Linux-x86_64.sh /tmp
RUN \
    # 更换apt源
    cp /etc/apt/sources.list /etc/apt/sources.list.bak \
    && sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    # 安装一些工具并配置ssh
    && apt-get update \
    && apt-get -y install sudo \
    && apt-get -y install wget \
    && apt-get -y install vim \
    && apt-get -y install screen \
    && apt-get -y install git \
    && DEBIAN_FRONTEND=noninteractive apt-get -y install ssh \
    && apt-get -y install openssh-server \
    && apt-get -y install openssh-client \
    # && sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config \ 
    # && sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config \
    && sed -i '$a\UsePAM no' /etc/ssh/sshd_config \
    && sed -i '$a\PermitRootLogin yes' /etc/ssh/sshd_config 
RUN \
    # 下载安装anaconda并配置虚拟环境
    cd /tmp \
    && sh Anaconda3-2023.09-0-Linux-x86_64.sh -b -p /opt/anaconda3 \
    && /opt/anaconda3/bin/conda init \
    && export PATH="/opt/anaconda3/bin":$PATH \
    && conda create -n dev python=3.8 -y \
    && source activate dev \
    && pip3 install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 install tqdm yacs opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 install opencv-python-headless -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && conda install linux-64_gdal-2.4.4-py38hfe926b7_1.tar.bz2 \
    && conda install gdal \
    # 清理
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/*
# RUN \
#     # 下载安装miniconda并配置虚拟环境
#     cd /tmp \
#     && sh Miniconda3-py310_23.5.1-0-Linux-x86_64.sh -b -p /opt/miniconda3 \
#     && /opt/miniconda3/bin/conda init \
#     && export PATH="/opt/miniconda3/bin":$PATH \
#     && conda create -n dev python=3.8 -y \
#     && source activate dev \
#     && pip3 install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple \
#     && pip3 install tqdm yacs opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple \
#     && pip3 install opencv-python-headless -i https://pypi.tuna.tsinghua.edu.cn/simple \
#     && conda install linux-64_gdal-2.4.4-py38hfe926b7_1.tar.bz2 \
#     && conda install gdal \
#     # 清理
#     && apt-get clean \
#     && rm -rf /tmp/* /var/tmp/*

EXPOSE 22

CMD ["/bin/bash"]
