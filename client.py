import socket
import os
import time
import sys
import threading

# Get server IP and keepalive interval from command line arguments
if len(sys.argv) > 1:
    SERVER_IP = sys.argv[1]
else:
    SERVER_IP = '127.0.0.1'
INTERVAL = int(sys.argv[2]) if len(sys.argv) > 2 else 30
SERVER_PORT = 2667

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)  # 1 second timeout for recv

print(f"[DEBUG] Client started. Sending keepalive to {SERVER_IP}:{SERVER_PORT} every {INTERVAL} seconds. Listening for incoming packets. Press Ctrl+C to stop.")

stop_event = threading.Event()
t1 = None
t2 = None

def listen():
    while not stop_event.is_set():
        try:
            data, addr = sock.recvfrom(1024)
            try:
                decoded = data.decode()
                print(f"[RECV] {decoded} from {addr}")
            except UnicodeDecodeError:
                print(f"[RECV] {len(data)} bytes (non-text) from {addr}")
        except socket.timeout:
            continue

def keepalive():
    while not stop_event.is_set():
        message = os.urandom(32)
        sock.sendto(message, (SERVER_IP, SERVER_PORT))
        print(f"[SEND] {len(message)} bytes of random data to {SERVER_IP}:{SERVER_PORT}")
        for _ in range(INTERVAL):
            if stop_event.is_set():
                break
            time.sleep(1)

try:
    t1 = threading.Thread(target=listen, daemon=True)
    t2 = threading.Thread(target=keepalive, daemon=True)
    t1.start()
    t2.start()
    while t1.is_alive() and t2.is_alive():
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nInterrupted by user")
    stop_event.set()
    if t1:
        t1.join()
    if t2:
        t2.join()
finally:
    sock.close()
