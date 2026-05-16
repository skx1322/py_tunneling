import socket
import ssl
import threading

PUBLIC_WEB_PORT = 8443   
DESKTOP_PIPE_PORT = 9000  

client_tunnel_sock = None  

def forward_stream(source, destination):
    """Pipes data from source socket to destination socket."""
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

def handle_public_request(public_ssl_sock):
    """Takes public HTTPS requests and forwards them down the desktop pipe."""
    global client_tunnel_sock
    if client_tunnel_sock is None:
        print("[-] Error: Desktop client is not connected yet. Cannot forward traffic.")
        public_ssl_sock.close()
        return

    print("[+] Forwarding public request down to the desktop API...")

    t1 = threading.Thread(target=forward_stream, args=(public_ssl_sock, client_tunnel_sock))
    t2 = threading.Thread(target=forward_stream, args=(client_tunnel_sock, public_ssl_sock))
    t1.start()
    t2.start()

def accept_desktop_client():
    """Listens for your desktop client to connect and establish the tunnel pipe."""
    global client_tunnel_sock
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    control_socket.bind(('0.0.0.0', DESKTOP_PIPE_PORT))
    control_socket.listen(1)
    print(f"[*] Control Port open on {DESKTOP_PIPE_PORT}. Awaiting desktop client.py...")
    
    client_tunnel_sock, addr = control_socket.accept()
    print(f"[+] Desktop client connected successfully from {addr}. Tunnel is active!")

def start_gateway():
    threading.Thread(target=accept_desktop_client, daemon=True).start()

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    public_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    public_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    public_socket.bind(('0.0.0.0', PUBLIC_WEB_PORT))
    public_socket.listen(20)
    print(f"[*] Public Gateway listening securely on HTTPS://0.0.0.0:{PUBLIC_WEB_PORT}")

    while True:
        try:
            raw_sock, addr = public_socket.accept()
            ssl_sock = context.wrap_socket(raw_sock, server_side=True)
            
            req_thread = threading.Thread(target=handle_public_request, args=(ssl_sock,))
            req_thread.daemon = True
            req_thread.start()
        except Exception as e:
            print(f"[-] SSL Handshake or Connection error: {e}")

if __name__ == "__main__":
    start_gateway()