import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_CONFIG = {
    "TUNNEL_ADDRESS": str(os.getenv("TUNNEL_CLOUD_ADDRESS")) or '127.0.0.1',
    "TUNNEL_PORT": int(os.getenv("TUNNEL_CLOUD_PORT")) or 9000,
    "TARGET_ADDRESS": str(os.getenv("LOCAL_TARGET_ADDRESS")) or '127.0.0.1',
    "TARGET_PORT": int(os.getenv("LOCAL_TARGET_PORT")) or 8080,
}

SERVER_CONFIG = {
    "TUNNEL_OPEN_PORT": int(os.getenv("TUNNEL_CLOUD_PORT")) or 9000,
    "FORWARD_PORT": int(os.getenv("TUNNEL_FORWARD_PORT")) or 8080,
}

print(SERVER_CONFIG['TUNNEL_OPEN_PORT'])
print(SERVER_CONFIG["FORWARD_PORT"])