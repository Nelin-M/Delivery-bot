"""
Initializing dispatcher on users commands
"""
# pylint: disable-all

from .enter_menu import dispatcher
from .main_menu import dispatcher
from .my_car import dispatcher
from .ride_request_creation import dispatcher
from .feedback import dispatcher
from .my_ride_requests import dispatcher
from .subscribes import dispatcher
from .complaint import dispatcher

__all__ = ["dispatcher"]
