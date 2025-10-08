import socket
import time
import threading

LOCAL_IP = '0.0.0.0'  # Listen on all interfaces
LOCAL_PORT = 2667

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LOCAL_IP, LOCAL_PORT))
print(f"Server listening on {LOCAL_IP}:{LOCAL_PORT}")

sending = False
stream_addr = None
last_received = time.time()
TIMEOUT = 60  # Stop streaming if no packet received for 60 seconds

def send_stream():
    global sending, stream_addr, last_received
    i = 0
    while sending:
        if time.time() - last_received > TIMEOUT:
            print(f"[DEBUG] Timeout: No packets received for {TIMEOUT} seconds. Stopping stream.")
            sending = False
            break
        if stream_addr:
            response = f'Packet {i} from server'.encode()
            sock.sendto(response, stream_addr)
            print(f"[DEBUG] Sent: {response.decode()} to {stream_addr}")
            i += 1
        time.sleep(0.3)

while True:
    # Receive packet
    data, addr = sock.recvfrom(1024)
    print(f"[DEBUG] Received {len(data)} bytes from {addr}: {data}")
    last_received = time.time()
    
    if not sending:
        sending = True
        stream_addr = addr
        threading.Thread(target=send_stream, daemon=True).start()
        print(f"[DEBUG] Started streaming to {addr}")
