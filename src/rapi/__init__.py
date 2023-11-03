"""
The client and domain model to work with schedule, stations , shows, episodes, participants, persons.
"""

from rapi._client import Client as Client
from rapi._domain import Show as Show
from rapi._domain import Station as Station

__all__ = ("Client", "Station", "Show")

__version__ = "0.10.0"
