import socket


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the local machine name
    host = 'localhost'
    port = 12333  # Reserve a port for your service.

    # Bind to the port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    # Wait for a connection
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive data from the client
    data = client_socket.recv(1024)
    print(f"Received data: {data.decode('utf-8')}")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_server()