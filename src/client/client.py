import pickle
import socket

from src.constants.network_constants import ADDRESS


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect(ADDRESS)

    def send(self, data):
        self.socket.send(pickle.dumps(data))

    def receive(self): ...
