import socket
import os
from dotenv import load_dotenv, dotenv_values
import time

from utils.wait_for_match import wait_for_match
from firstGame import run_game

load_dotenv()

HOST = os.getenv("HOST") or "127.0.0.1"
PORT = int(os.getenv("PORT") or 5555)   

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

player_id = wait_for_match(client)
run_game(client, player_id)

