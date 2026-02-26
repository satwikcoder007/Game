import socket
import threading
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

HOST = os.getenv("HOST") or "127.0.0.1"   # local machine
PORT = int(os.getenv("PORT") or 5555)          # any free port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print(f"Server running on http://{HOST}:{PORT}")

def handle_client(conn, addr):
    print(f"Player connected from {addr}")
    
    response_body = "Hello from your Python server 👋"
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n"
        f"{response_body}"
    )
    conn.sendall(response.encode("utf-8"))
    conn.close()

def start():  ## main server loop
    while True:
        conn, addr = server.accept() ## wait for a new client connection i.e. a player hit the derault route of the server
        thread = threading.Thread(target=handle_client, args=(conn, addr)) ## create a new thread to handle furthur action without blocking the main server loop
        thread.start()

start()