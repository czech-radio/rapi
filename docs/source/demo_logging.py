import logging

from rapi import Client

client = Client()

logging.basicConfig(level=logging.DEBUG)

client.get_station("11")
