import socket
import threading
import os
import time
from dotenv import load_dotenv, dotenv_values

from utils.match_making import match_making

load_dotenv()

HOST = os.getenv("HOST") or "127.0.0.1"   
PORT = int(os.getenv("PORT") or 5555)         

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server running on http://{HOST}:{PORT}")

##This one is just for testng
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


lobby = []
matches = []
player_to_match = {}
lobby_lock = threading.Lock()  

def match_making_loop():
    while True:
        with lobby_lock:
            match_making(lobby, matches, player_to_match)
        time.sleep(3)

def start():  ## main server loop
    mythread = threading.Thread(target=match_making_loop, daemon=True)
    mythread.start()
    while True:
        conn, addr = server.accept() ## wait for a new client connection i.e. a player hit the derault route of the server
        with lobby_lock:
            lobby.append(conn) ## add the player to the lobby
start()