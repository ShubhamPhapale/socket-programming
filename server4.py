import socket
import select
import sys

def main():
    # Get server IP and port from command line arguments
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <server-ip-addr> <server-port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified IP and port
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections
    server_socket.listen()

    print("Echo Server listening on {}:{}".format(server_ip, server_port))

    # List to keep track of connected clients
    clients = [server_socket]

    try:
        while True:
            # Use select to check for readable sockets
            readable, _, _ = select.select(clients, [], [])

            for readable_socket in readable:
                if readable_socket == server_socket:
                    # Accept a new connection from a client
                    client_socket, client_address = server_socket.accept()
                    print(f"Connected with client {client_socket.fileno()}")

                    # Add the new client socket to the list
                    clients.append(client_socket)

                else:
                    # Handle data from an existing client
                    data = readable_socket.recv(1024)
                    if not data:
                        # If no data received, client disconnected
                        print(f"Client {readable_socket.fileno()} disconnected.")
                        clients.remove(readable_socket)
                        readable_socket.close()
                    else:
                        # Echo the received message back to the client
                        print(f"Received from client {readable_socket.fileno()}: {data.decode()}")
                        readable_socket.sendall(data)

    except OSError as e:
        if e.errno == 48:  # Error code 48: Address already in use
            print("Error: Another server is already running on the specified port.")
        else:
            print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        # Close all client sockets
        for client_socket in clients[1:]:
            client_socket.close()

        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    main()
