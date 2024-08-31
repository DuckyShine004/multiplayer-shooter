import time
import pickle
import socket
import threading

from threading import Event

from src.server.network.resource import Resource
from src.common.constants.network_constants import ADDRESS


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = -1
        self.resources = None
        self.is_running = True
        self.latency = 0
        self.id_event = Event()

    def connect(self):
        self.socket.connect(ADDRESS)

        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

    def ping(self):
        try:
            start_time = time.time()
            self.send({"type": "ping"})
            while True:
                if not self.resources:
                    continue

                resource = next(iter(self.resources.values()))

                if not isinstance(resource, Resource):
                    continue

                if self.resources[self.id].get_entity("pong"):
                    end_time = time.time()
                    self.latency = end_time - start_time
                    break
        except socket.error as socket_error:
            print(f"Error pinging server: {socket_error}")

    def send(self, data):
        self.socket.send(pickle.dumps(data))

    def receive(self):
        try:
            while self.is_running:
                data = self.socket.recv(1 << 32)

                if data:
                    self.resources = pickle.loads(data)

                    if self.id == -1:
                        self.id = self.resources.get("id", -1)
                        self.id_event.set()
        except socket.error as socket_error:
            self.is_running = False
            print("Error:", socket_error)

    def wait_for_id_from_server(self):
        self.id_event.wait()

    def get_resources(self):
        return self.resources
