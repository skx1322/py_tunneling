from service.tunnel import start_tunnel_client
from config.host import CLIENT_CONFIG

# if __name__ == "__main__":
#     start_tunnel_client(**CLIENT_CONFIG)

if __name__ == "__main__":
    start_tunnel_client(CLIENT_CONFIG["TUNNEL_ADDRESS"], CLIENT_CONFIG["TUNNEL_PORT"], CLIENT_CONFIG["TARGET_PORT"])
