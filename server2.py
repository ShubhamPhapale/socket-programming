import socket
import threading
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

            print(f"Client {threading.current_thread().name} sent message:", client_message)

            # Validate the client's message
            if not is_valid_expression(client_message):
                error_message = "Error: Invalid input. Please enter a valid arithmetic expression."
                client_socket.sendall(error_message.encode())
                print(f"Sending reply to {threading.current_thread().name}:", error_message)
                continue

            # Process the message (evaluate arithmetic expression)
            result = eval(client_message)

            # Send the result back to the client
            client_socket.sendall(str(result).encode())
            print(f"Sending reply to {threading.current_thread().name}:", result)

    except ConnectionResetError:
        print(f"Client {threading.current_thread().name} disconnected.")
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

    try:
        # Bind the socket to the specified IP and port
        server_socket.bind((server_ip, server_port))

        # Listen for incoming connections
        server_socket.listen()

        print("Server listening on {}:{}".format(server_ip, server_port))

        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print(f"Connected with client {client_address}")

            # Create a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
            client_thread.start()

    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    main()
