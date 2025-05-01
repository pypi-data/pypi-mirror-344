import pandas as pd

import importlib.resources as pkg_resources
from . import data  # 确保 src/cfun/data/__init__.py 存在
from . import dx


ALL_FREQUENCY_PATH = pkg_resources.files(data).joinpath("all_frequency.parquet")

DX_DET_PATH = pkg_resources.files(dx).joinpath("dx_det.onnx")
DX_CLS_PATH = pkg_resources.files(dx).joinpath("dx_cls.onnx")


__all__ = [
    "ALL_FREQUENCY_PATH",
    "DX_DET_PATH",
    "DX_CLS_PATH",
]