import socket

# Server settings
SERVER_HOST = "0.0.0.0"  # Bind to all interfaces
SERVER_PORT = 8080
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)

# Create and bind server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(SERVER_ADDRESS)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
except Exception as e:
    print(f"Failed to bind the server socket: {e}")
    exit(1)

# Start listening for incoming connections
server.listen()

while True:
    try:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client.send("Hello World".encode())  # Send message to client
        print("Message sent to client: 'Hello World'")
        print(client.recv(1024).decode())  # Receive message from client
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        continue
