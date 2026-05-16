import socket
import ssl
import threading
from host import port, server_ip

TARGET_TCP_HOST = '127.0.0.1'
TARGET_TCP_PORT = 8080

def forward_stream(src_sock, dest_sock):
    try:
        while True:
            data = src_sock.recv(4096)
            if not data:
                break
            dest_sock.sendall(data)
    except Exception as e:
        print(f"Forwarding exception: {e}")
    finally: 
        try:
            src_sock.close()
        except:
            pass
        try:
            dest_sock.close()
        except:
            pass

def handle_client(client_ssl_socket):
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        target_socket.connect((TARGET_TCP_HOST, TARGET_TCP_PORT))
        print(f"Successfully tunneled to target server at {TARGET_TCP_HOST}:{TARGET_TCP_PORT}")

        client_to_target = threading.Thread(target=forward_stream, args=(client_ssl_socket, target_socket))
        target_to_client = threading.Thread(target=forward_stream, args=(target_socket, client_ssl_socket))
        
        client_to_target.start()
        target_to_client.start()
        
    except Exception as e:
        print(f"Failed to connect to target application: {e}")
        client_ssl_socket.close()

def start_vpn_server(host, port):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsocket.bind((host, port))
    bindsocket.listen(10)

    print(f"VPN Tunnel Server listening securely on {host}:{port}")

    while True:
        try:
            newsocket, fromaddr = bindsocket.accept()
            print(f"Secure connection request from {fromaddr}")
            conn = context.wrap_socket(newsocket, server_side=True)
            
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.daemon = True
            client_thread.start()
            
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    start_vpn_server(server_ip, port)