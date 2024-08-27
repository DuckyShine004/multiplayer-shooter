import socket
import pickle
import threading


from src.server.network.resource import Resource
from src.constants.network_constants import ADDRESS


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.resources = {}
        self.client_id = 0

    def start_client_thread(self, connection):
        client_id = self.add_client(connection)
        target = self.handle_client
        arguments = (connection, client_id)

        thread = threading.Thread(target=target, args=arguments)
        thread.start()

    def add_client(self, connection):
        resource = Resource()
        resource.initialise()

        client_id = self.client_id
        self.clients[client_id] = connection
        self.resources[client_id] = resource
        self.client_id += 1

        return client_id

    def send_resources(self):
        resources = pickle.dumps(self.resources)

        for connection in self.clients.values():
            connection.send(resources)

    def remove_client(self, client_id):
        print(f"Client {client_id} disconnected")
        self.clients.pop(client_id)
        self.resources.pop(client_id)

    def handle_client(self, connection, client_id):
        try:
            while True:
                data = connection.recv(2048)

                if not data:
                    break

                self.process_data(client_id, data)
        finally:
            self.remove_client(client_id)
            connection.close()

    def process_data(self, client_id, data):
        data = pickle.loads(data)
        resource = self.resources[client_id]

        if data["type"] == "move":
            player = resource.get_entity("player")
            player.move(data["dx"], data["dy"])

        self.send_resources()

    def run(self):
        self.socket.bind(ADDRESS)
        self.socket.listen()
        print("Opening server connection")

        try:
            while True:
                connection, address = self.socket.accept()
                print(f"Connected by {address}")

                self.start_client_thread(connection)
        finally:
            self.socket.close()


server = Server()
server.run()
