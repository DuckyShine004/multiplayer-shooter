import socket
import pickle
import threading

from threading import Lock


from src.server.network.resource import Resource
from src.common.constants.network_constants import ADDRESS


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.resources = {}
        self.messages = []
        self.client_id = 0
        self.lock = Lock()

    def start_client_thread(self, connection):
        with self.lock:
            client_id = self.client_id
            self.client_id += 1

        thread = threading.Thread(target=self.handle_client, args=(client_id, connection))
        thread.start()

    def add_client(self, client_id, connection):
        with self.lock:
            self.clients[client_id] = connection
            resource = Resource()
            resource.initialise()
            self.resources[client_id] = resource

        self.add_server_message(f"SERVER: {client_id} joined the server")
        self.send_data_to_client(client_id, {"id": client_id})

    def add_server_message(self, message):
        self.messages.append(message)
        self.set_all_resources("messages", self.messages)

    def send_data_to_client(self, client_id, data):
        data = pickle.dumps(data)

        with self.lock:
            self.clients[client_id].send(data)

    def send_data_to_all_clients(self, data):
        data = pickle.dumps(data)

        with self.lock:
            for connection in self.clients.values():
                connection.send(data)

    def remove_client(self, client_id):
        with self.lock:
            connection = self.clients.pop(client_id)

            if connection:
                connection.close()

            self.resources.pop(client_id)

        print(f"Client {client_id} disconnected")
        self.add_server_message(f"SERVER: {client_id} disconnected")

    def handle_client(self, client_id, connection):
        self.add_client(client_id, connection)

        try:
            while True:
                data = connection.recv(2048)

                if not data:
                    break

                self.process_data(client_id, data)
        finally:
            self.remove_client(client_id)

    def process_data(self, client_id, data):
        data = pickle.loads(data)
        resource = self.resources[client_id]

        if data["type"] == "move":
            player = resource.get_entity("player")
            player.move(data["dx"], data["dy"])

        if data["type"] == "message":
            self.add_server_message(data["message"])

        self.send_data_to_all_clients(self.resources)

    def set_all_resources(self, entity_name, data):
        for resource in self.resources.values():
            resource.set_entity(entity_name, data)

    def run(self):
        self.socket.bind(ADDRESS)
        self.socket.listen()
        print("Server started!")

        try:
            while True:
                connection, address = self.socket.accept()
                print(f"Connected by {address}")

                self.start_client_thread(connection)
        finally:
            self.socket.close()


if __name__ == "__main__":
    server = Server()
    server.run()
