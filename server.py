import socket

LOCAL_IP = '0.0.0.0'  # Listen on all interfaces
LOCAL_PORT = 2666

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LOCAL_IP, LOCAL_PORT))
print(f"Server listening on {LOCAL_IP}:{LOCAL_PORT}")

while True:
    # Receive packet
    data, addr = sock.recvfrom(1024)
    print(f"Received {len(data)} bytes from {addr}")
    
    # Send response back to sender
    response = b'hi from the server'
    sock.sendto(response, addr)
    print(f"Sent: {response.decode()} to {addr}")
