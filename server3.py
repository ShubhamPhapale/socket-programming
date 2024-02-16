import socket
import select
import re
import sys

def is_valid_expression(expression):
    # Use regular expression to check if the input is a valid arithmetic expression
    pattern = re.compile(r'^\s*\d+(\s*[+\-*/]\s*\d+)*\s*$')
    return bool(pattern.match(expression))

def handle_client(client_socket, clients):  
    # Receive client's message
    client_message = client_socket.recv(1024).decode()
    if not client_message:
        # If no data received, client disconnected
        print(f"Client {client_socket.fileno()} disconnected.")
        clients.remove(client_socket)
        client_socket.close()
        clients.remove(client_socket)
        return

    else :
        print(f"Client {client_socket.fileno()} sent message:", client_message)

        # Validate the client's message
        if not is_valid_expression(client_message):
            error_message = "Error: Invalid input. Please enter a valid arithmetic expression."
            client_socket.sendall(error_message.encode())
            print(f"Sending reply to {client_socket.fileno()}:", error_message)
            return
            
        # Process the message (evaluate arithmetic expression)
        result = eval(client_message)

        # Send the result back to the client
        client_socket.sendall(str(result).encode())
        print(f"Sending reply to {client_socket.fileno()}:", result)

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

    print("Server listening on {}:{}".format(server_ip, server_port))

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
                    handle_client(readable_socket, clients)

    except OSError as e:
        if e.errno == 48:  # Error code 48: Address already in use
            print("Error: Another server is already running on the specified port.")
        else:
            print(f"Error: {e}")
    except ConnectionResetError:
        print(f"Client {client_socket.fileno()} disconnected.")
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

