from service.tunnel import open_gateway
from config.host import SERVER_CONFIG

if __name__ == "__main__":
    open_gateway(SERVER_CONFIG["TUNNEL_OPEN_PORT"], SERVER_CONFIG["FORWARD_PORT"])
