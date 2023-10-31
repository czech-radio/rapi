"""
The client and domain model to work with schedule, stations , shows, episodes, participants, persons.
"""

from rapi._client import Client as Client
from rapi._model import Station as Station
from rapi._model import Show as Show

__all__ = ("Client", "Station", "Show")

__version__ = "0.9.0"
