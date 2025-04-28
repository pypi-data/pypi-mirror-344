# neural_lowthrust/__init__.py

# 把生成的 nn_lowthrust 扩展模块当作子模块导入
from . import nn_lowthrust as _ext

# 把所有公开的符号扔到包顶层
globals().update(_ext.__dict__)
__all__ = [name for name in globals() if not name.startswith("_")]

# 版本号保持一致
__version__ = "0.1.0"
