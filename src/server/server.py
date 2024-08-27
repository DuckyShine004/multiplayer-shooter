import socket
import pickle
import threading


from src.server.network.resource import Resource
from src.constants.network_constants import ADDRESS


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.resources = {}
        self.resource_id = 0

    def add_resource(self):
        resource = Resource()
        resource.initialise()

        self.resources[self.resource_id] = resource
        resource_id = self.resource_id
        self.resource_id += 1

        return resource_id

    def remove_resource(self, resource_id):
        print(f"Client {resource_id} disconnected")
        self.resources.pop(resource_id)

    def handle_resource(self, connection, resource_id):
        try:
            while True:
                data = connection.recv(2048)

                if not data:
                    break

                self.process_data(resource_id, data)
        finally:
            self.remove_resource(resource_id)
            connection.close()

    def process_data(self, resource_id, data):
        data = pickle.loads(data)
        print(data)
        resource = self.resources[resource_id]

        if data["type"] == "move":
            player = resource.get_entity("player")
            player.move(data["dx"], data["dy"])

    def run(self):
        self.socket.bind(ADDRESS)
        self.socket.listen()
        print("Opening server connection")

        try:
            while True:
                connection, address = self.socket.accept()
                print(f"Connected by {address}")

                resource_id = self.add_resource()

                thread = threading.Thread(target=self.handle_resource, args=(connection, resource_id))
                thread.start()
        finally:
            self.socket.close()


server = Server()
server.run()
