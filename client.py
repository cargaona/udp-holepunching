import socket
import os
import time

import sys

# Get server IP from command line argument or default to localhost
if len(sys.argv) > 1:
    SERVER_IP = sys.argv[1]
else:
    SERVER_IP = '127.0.0.1'
SERVER_PORT = 2666

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)  # 1 second timeout for recv

print(f"Sending random data to {SERVER_IP}:{SERVER_PORT}. Press Ctrl+C to stop.")

try:
    while True:
        # Generate random data (32 bytes)
        message = os.urandom(32)
        sock.sendto(message, (SERVER_IP, SERVER_PORT))
        print(f"Sent {len(message)} bytes of random data")
        
        # Try to receive response
        try:
            data, addr = sock.recvfrom(1024)
            try:
                decoded = data.decode()
                print(f"Received: {decoded} from {addr}")
            except UnicodeDecodeError:
                print(f"Received {len(data)} bytes (non-text) from {addr}")
        except socket.timeout:
            pass  # No response, continue
        
        time.sleep(1)  # Wait 1 second before next send
except KeyboardInterrupt:
    print("\nInterrupted by user")

sock.close()
