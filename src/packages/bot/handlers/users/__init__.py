"""
Initializing dispatcher on users commands
"""
# pylint: disable-all

from .enter_menu import dispatcher
from .main_menu import dispatcher
from .profile import dispatcher


__all__ = ["dispatcher"]
