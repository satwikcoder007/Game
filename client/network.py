import socket
import os
from dotenv import load_dotenv, dotenv_values
import time
import threading
from utils.wait_for_match import wait_for_match
from utils.receive_message import receive_message
import queue

load_dotenv()

HOST = os.getenv("HOST") or "127.0.0.1"
PORT = int(os.getenv("PORT") or 5555)   

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    player_id = wait_for_match(client)

    oponent_queue = queue.Queue() ## surprisingly these are thread safe

    threading.Thread(target=receive_message, args=(client,oponent_queue,), daemon=True).start()
    
    return client, player_id, oponent_queue
