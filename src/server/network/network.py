import pickle
import socket

from src.client.client import Client
from src.constants.network_constants import ADDRESS
from src.server.server import Server


class Network:
    def __init__(self):
        self.client = Client()
        self.server = Server()

    def run(self):
        self.server.run()
        self.client.connect()

    def send(self, data):
        self.client.send(data)

    def receive(self): ...
