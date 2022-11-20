"""
Initialization file for the package __loggers__.
"""
from .logger import *

# pylint: disable=E0602,E0603
__all__ = ["Log", "logger", "Loggers"]

logger = Log()
