import socket
import threading
from py_tunneling.legacy.host import server_ip, pipe_port, local_port
CLOUD_IP =  server_ip
CLOUD_PIPE_PORT = pipe_port             
LOCAL_API_PORT = local_port           

def forward_stream(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.sendall(data)
    except Exception:
        pass
    finally:
        source.close()
        destination.close()

def start_tunnel_client():
    print(f"[*] Connecting to Cloud Tunnel at {CLOUD_IP}:{CLOUD_PIPE_PORT}...")
    
    cloud_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cloud_sock.connect((CLOUD_IP, CLOUD_PIPE_PORT))
        print("[+] Established connection to cloud tunnel.")
    except Exception as e:
        print(f"[-] Connection failed: {e}. Is server.py running on the cloud?")
        return

    local_api_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        local_api_sock.connect(('127.0.0.1', LOCAL_API_PORT))
        print(f"[+] Connected to local API on port {LOCAL_API_PORT}.")
    except Exception as e:
        print(f"[-] Failed to reach local API on port {LOCAL_API_PORT}. Ensure your API server is turned on!")
        cloud_sock.close()
        return

    print("[*] Tunnel routing online. Data is flowing.")
    t1 = threading.Thread(target=forward_stream, args=(cloud_sock, local_api_sock))
    t2 = threading.Thread(target=forward_stream, args=(local_api_sock, cloud_sock))
    t1.start()
    t2.start()

if __name__ == "__main__":
    start_tunnel_client()