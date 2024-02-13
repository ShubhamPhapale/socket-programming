import socket
import sys

def main():
    # Get server IP and port from command line arguments
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <server-ip-addr> <server-port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    # Create client socket
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server
        sockfd.connect((server_ip, server_port))
        print("Connected to server")

        while True:
            # Ask user for message to send to server
            user_input = input("Please enter the message to the server: ")

            # Write to server
            sockfd.sendall(user_input.encode())

            # Read reply with a timeout
            try:
                sockfd.settimeout(1)
                server_reply = sockfd.recv(1024).decode()
                if not server_reply:
                    print("ERROR reading from socket")
                else:
                    print("Server replied:", server_reply)
                    sockfd.settimeout(None)

            except socket.timeout:
                print("Server Busy. Please Wait...")

                # Wait for the reply without a timeout
                sockfd.settimeout(None)
                server_reply = sockfd.recv(1024).decode()
                print("Holaa..!! Server now serves You!!\nServer replied:", server_reply)

    except KeyboardInterrupt:
        print("Client terminated by user.")
    except socket.error as e:
        print(f"Socket error: {e}")
    except ValueError:
        print("Error: Invalid port number.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        sockfd.close()

if __name__ == "__main__":
    main()
