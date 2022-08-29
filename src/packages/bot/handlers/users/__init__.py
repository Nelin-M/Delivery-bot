"""
Initializing the dispatcher from modules
"""
# pylint: disable-all

from .commands_for_admins import dispatcher
from .commands_for_users import dispatcher
from .cancel import dispatcher
from .errors import dispatcher


__all__ = ["dispatcher"]
