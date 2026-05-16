import os
from dotenv import load_dotenv

load_dotenv()

port = int(os.getenv("CLIENT_PORT"))
server_ip = os.getenv("SERVER_IP")

print(f"Connecting to port {port} using key: {server_ip}")