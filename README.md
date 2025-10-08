# UDP Hole Punching POC

This is a simple proof-of-concept for UDP hole punching / NAT traversal using Python.

## How it works
- **Server** listens for UDP packets on port 2667. After receiving the first packet from a client, it starts sending a continuous stream of packets every 0.3 seconds to that client. It stops streaming if no packets are received from the client for 30 seconds.
- **Client** runs two threads: one listens continuously for incoming packets and prints them, the other sends keepalive packets (32 bytes of random data) at a configurable interval (default 30 seconds) to maintain the NAT hole.

## Usage

### 1. Start the server
On the server (public IP or port-forwarded):
```sh
python server.py
```

### 2. Start the client
On the client (behind NAT or anywhere):
```sh
python client.py <server_ip> <keepalive_interval_seconds>
```
- `<server_ip>`: IP of the server (required).
- `<keepalive_interval_seconds>`: Interval for sending keepalives (optional, default 30).
- Example:
  ```sh
  python client.py 203.0.113.1 10
  ```

## Stopping
- Press `Ctrl+C` to stop the client.
- The server stops streaming automatically after 30 seconds of no client packets.

## Notes
- The client sends keepalive packets to keep the NAT mapping open.
- The server sends a numbered packet stream (e.g., "Packet 1 from server") every 0.3 seconds once started.
- This demonstrates UDP NAT traversal with keepalives and streaming.
- No external dependencies; uses Python standard library.
