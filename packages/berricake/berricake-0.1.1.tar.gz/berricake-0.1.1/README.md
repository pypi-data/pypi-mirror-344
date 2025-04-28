# 软件名称

## <u>BerriCake</u>

## 概述

本软件依赖于 `scipy` 和 `numpy` 等科学计算库，以下是详细的安装和使用说明。

## 环境要求

- Python 3.x
- `pip` 包管理工具

```
colorama==0.4.6
Cython==3.0.12
numpy==2.2.5
scipy==1.15.2
setuptools==79.0.0
```

## 安装程序

```commandline
pip install barricake
```



## 代码示例

```
from core.berricake import BerriCake


if __name__ == "__main__":
    file_path = 'in.txt'
   
    # 创建 Manager 实例
    bc = BerriCake(file_path)
    bc.run()   #运行
```



# 软件开发者

## 安装步骤

### 1. 安装必要的依赖包

首先，确保你已经安装了 `setuptools` 和 `Cython`。可以使用以下命令进行安装：

```bash
pip install setuptools
pip install Cython -i https://mirrors.aliyun.com/pypi/simple/
```

### 2. 编译程序

进入项目目录，执行编译命令：

```bash
python setup.py build_ext --inplace
```

### 3. 安装 `scipy` 和 `numpy`

使用 `pip` 安装 `scipy` 和 `numpy`：

```bash
pip install scipy numpy
```



# 更新日志



 2025-4-28 `0.1.0`  第一个发布版本  
