import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_CONFIG = {
    "TUNNEL_ADDRESS": str(os.getenv("TUNNEL_CLOUD_ADDRESS")),
    "TUNNEL_PORT": int(os.getenv("TUNNEL_CLOUD_PORT")),
    "TARGET_PORT": int(os.getenv("LOCAL_TARGET_PORT")) or '127.0.0.1',
    "TARGET_ADDRESS": str(os.getenv("LOCAL_TARGET_ADDRESS")),
}
