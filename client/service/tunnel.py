import socket
import threading
import ssl

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

def start_tunnel_client(CLOUD_IP, CLOUD_PIPE_PORT, TARGET_PORT, TARGET_ADDRESS = '127.0.0.1'):
    print(f"Target Address: {TARGET_ADDRESS}:{TARGET_PORT}\nCloud Address: {CLOUD_IP}:{CLOUD_PIPE_PORT}")

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    try:
        context.load_verify_locations(cafile="server.crt")
        context.check_hostname = False
    except Exception as e:
        print(f"{e}")
        return

    raw_cloud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cloud_sock = context.wrap_socket(raw_cloud_socket, server_hostname=CLOUD_IP)

        cloud_sock.connect((CLOUD_IP, CLOUD_PIPE_PORT))
        print(f"[+] Established connection to cloud tunnel by {CLOUD_IP}:{CLOUD_PIPE_PORT}")
    except Exception as e:
        print(f"[-] Connection failed: {e}.")
        return

    local_api_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        local_api_sock.connect((TARGET_ADDRESS, TARGET_PORT))
        print(f"[+] Connected to local API on port {TARGET_ADDRESS}:{TARGET_PORT}.")
    except Exception as e:
        print(f"[-] Failed to reach local API on {TARGET_ADDRESS}:{TARGET_PORT}: {e}")
        cloud_sock.close()
        return

    print(f"Forwarding Address: {TARGET_ADDRESS}:{TARGET_PORT} => Cloud Address: {CLOUD_IP}:{CLOUD_PIPE_PORT}")
    t1 = threading.Thread(target=forward_stream, args=(cloud_sock, local_api_sock))
    t2 = threading.Thread(target=forward_stream, args=(local_api_sock, cloud_sock))
    t1.start()
    t2.start()