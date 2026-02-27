import socket
import os
from dotenv import load_dotenv, dotenv_values
import time

load_dotenv()

HOST = os.getenv("HOST") or "127.0.0.1"
PORT = int(os.getenv("PORT") or 5555)   

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to server. Type messages:")

time.sleep(5)  # Wait for the server to be ready

msg = "can i play"
client.send(msg.encode())

data = client.recv(1024)
print("Received:", data.decode())