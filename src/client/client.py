import pickle
import socket
import threading

from src.constants.network_constants import ADDRESS


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.resources = None
        self.is_running = True

    def connect(self):
        self.socket.connect(ADDRESS)

        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()

    def send(self, data):
        self.socket.send(pickle.dumps(data))

    def receive(self):
        try:
            while self.is_running:
                data = self.socket.recv(2048)
                if data:
                    self.resources = pickle.loads(data)
                else:
                    self.running = False
        except Exception as e:
            print("Error:", e)
            self.running = False

    def get_resources(self):
        return self.resources
