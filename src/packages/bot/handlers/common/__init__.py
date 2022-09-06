"""
Initializing dispatcher on common commands
"""
# pylint:disable=W0404
from .cancel import dispatcher
from .errors import dispatcher


__all__ = ["dispatcher"]
