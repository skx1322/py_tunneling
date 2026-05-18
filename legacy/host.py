import os
from dotenv import load_dotenv

load_dotenv()

port = int(os.getenv("TUNNEL_CLOUD_PORT"))
server_ip = os.getenv("TUNNEL_CLOUD_ADDRESS")

pipe_port = int(os.getenv("CLOUD_PIPE_PORT"))
local_port = int(os.getenv("LOCAL_TARGET_PORT"))

print(f"Connecting to port {port} using key: {server_ip}")