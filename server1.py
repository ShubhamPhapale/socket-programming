import socket
import re
import sys

def is_valid_expression(expression):
    # Use regular expression to check if the input is a valid arithmetic expression
    pattern = re.compile(r'^\s*\d+(\s*[+\-*/]\s*\d+)*\s*$')
    return bool(pattern.match(expression))

def handle_client(client_socket):
    try:
        while True:
            # Receive client's message
            client_message = client_socket.recv(1024).decode()
            if not client_message:
                print(f"Client {client_socket.fileno()} disconnected.")
                break

            print("Client sent message:", client_message)

            # Validate the client's message
            if not is_valid_expression(client_message):
                error_message = "Error: Invalid input. Please enter a valid arithmetic expression."
                client_socket.sendall(error_message.encode())
                print("Sending reply:", error_message)
                continue

            # Process the message (evaluate arithmetic expression)
            result = eval(client_message)

            # Send the result back to the client
            client_socket.sendall(str(result).encode())
            print("Sending reply:", result)
    
    except ConnectionResetError:
        print("Client disconnected.")
    finally:
        # Close the client socket
        client_socket.close()

def main():
    # Get server IP and port from command line arguments
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <server-ip-addr> <server-port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    current_client = None

    try:
        # Bind the socket to the specified IP and port
        server_socket.bind((server_ip, server_port))

        # Listen for incoming connections
        server_socket.listen()

        print("Server listening on {}:{}".format(server_ip, server_port))

        while True:
            # Accept a connection from a client
            if current_client == None :
                client_socket, client_address = server_socket.accept()
                print("Connected with client socket number", client_socket.fileno())

                # Set the current client
                current_client = client_socket

                # Handle the client in a separate function
                handle_client(client_socket)

                # Reset current client after handling
                current_client = None

    except OSError as e:
        if e.errno == 48:  # Error code 48: Address already in use
            print("Error: Another server is already running on the specified port.")
        else:
            print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    main()


