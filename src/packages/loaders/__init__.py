"""
Initialization file for the package __loaders__.
"""
from .config_loader import *

config = ConfigLoader.load_config()
env_variables = ConfigLoader.load_env_variables()

__all__ = ["config", "env_variables"]
