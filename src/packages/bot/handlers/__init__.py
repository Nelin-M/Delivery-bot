"""
Loads the dispatcher from packages
"""
# pylint:disable=W0404
from .users import dispatcher

# from .admins import dispatcher
from .common import dispatcher


__all__ = ["dispatcher"]
