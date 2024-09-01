import socket

# Client settings - use ngrok address
CLIENT_HOST = "0.tcp.au.ngrok.io"
CLIENT_PORT = 13516
CLIENT_ADDRESS = (CLIENT_HOST, CLIENT_PORT)

# Create client socket and connect to the server via ngrok
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(CLIENT_ADDRESS)
    print(f"Connected to server at {CLIENT_HOST}:{CLIENT_PORT}")
except Exception as e:
    print(f"Failed to connect to the server: {e}")
    exit(1)

try:
    # Receive message from server
    print(client.recv(1024).decode())
    # Send a message to the server
    client.send("Hey Server".encode())
    print("Message sent to server: 'Hey Server'")
    client.close()
except Exception as e:
    print(f"An error occurred during communication: {e}")
