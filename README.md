# Client-Server Socket Programming

## Introduction
This project implements client-server communication using socket programming in Python. It includes one client program and four server programs, each handling a different number of concurrent clients.

## Programs
- `client.py`: The client program
- `server1.py`: Handles one client at a time
- `server2.py`: Handles two clients concurrently
- `server3.py`: Handles three clients concurrently
- `server4.py`: Echo server handling multiple clients

## Features
- Arithmetic operations (+, -, *, /) with multiple operands
- Flexible input parsing (handles various spacing between operands and operators)
- Error handling for invalid operations
- Socket timeout for client-side server availability detection

## Running the Programs

### Server
```bash
python server#.py  # Replace # with 1, 2, 3, or 4
```

### Client
```bash
python client.py
```

## Additional Resources

- [YouTube Video](https://youtu.be/qstyrxJytZU)
- [My YouTube Channel](https://www.youtube.com/channel/UCzOmg9hOy3NBsScX--Nrb5Q)


## Testing
Comprehensive tests have been conducted to ensure:
1. Correct arithmetic operations
2. Proper handling of multiple clients
3. Graceful disconnection and reconnection
4. Error handling and edge cases

## Special Features
- Multi-operand arithmetic operations
- Flexible input parsing
- Robust error handling

## Notes
- The server uses file numbers to refer to clients, which may be the same for different clients.
- For `server1.py`, a timeout feature is implemented to handle busy server scenarios.

## Contributions
Contributions are welcome. Please fork the repository and submit a pull request with your changes.
