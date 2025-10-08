# UDP Hole Punching POC

This is a simple proof-of-concept for UDP hole punching / NAT traversal using Python.

## How it works
- **Server** listens for UDP packets on port 2666 and replies to any client.
- **Client** sends random UDP packets to the server and prints any response.

## Usage

### 1. Start the server
On the server (public IP or port-forwarded):
```sh
python server.py
```

### 2. Start the client
On the client (behind NAT or anywhere):
```sh
python client.py <server_ip>
```
- If `<server_ip>` is omitted, defaults to `127.0.0.1` (localhost).
- Example:
  ```sh
  python client.py 203.0.113.1
  ```

## Stopping
- Press `Ctrl+C` to stop the client.

## Notes
- The client sends 32 bytes of random data every second.
- The server replies with a text message to each packet.
- This demonstrates basic UDP NAT traversal (hole punching) for client-server.
