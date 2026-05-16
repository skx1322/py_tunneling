import socket
import ssl
import threading
from host import port, server_ip

LOCAL_LISTEN_PORT = 8080 

def forward_stream(source_sock, destination_sock):
    try:
        while True:
            data = source_sock.recv(4096)
            if not data:
                break
            destination_sock.sendall(data)
    except Exception:
        pass
    finally:
        source_sock.close()
        destination_sock.close()

def handle_local_connection(local_socket, vpn_host, vpn_port):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations("server.crt")
    context.check_hostname = False 

    try:
        raw_vpn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_vpn_socket.connect((vpn_host, vpn_port))
        ssl_vpn_socket = context.wrap_socket(raw_vpn_socket, server_hostname=vpn_host)
        
        t1 = threading.Thread(target=forward_stream, args=(local_socket, ssl_vpn_socket))
        t2 = threading.Thread(target=forward_stream, args=(ssl_vpn_socket, local_socket))
        
        t1.start()
        t2.start()
        print("Tunnel fully established for this session.")
    except Exception as e:
        print(f"Failed to build secure tunnel connection: {e}")
        local_socket.close()

def start_local_proxy(vpn_host, vpn_port):
    local_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_listener.bind(('127.0.0.1', LOCAL_LISTEN_PORT))
    local_listener.listen(5)
    print(f"Client-side tunnel endpoint open at 127.0.0.1:{LOCAL_LISTEN_PORT}")
    print(f"Traffic sent here will tunnel securely to the VPN at {vpn_host}:{vpn_port}")

    while True:
        local_socket, addr = local_listener.accept()
        proxy_thread = threading.Thread(target=handle_local_connection, args=(local_socket, vpn_host, vpn_port))
        proxy_thread.daemon = True
        proxy_thread.start()

if __name__ == "__main__":
    start_local_proxy(server_ip, port)