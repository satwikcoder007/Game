import json
from firstGame import run_game
def wait_for_match(client):
    while True:
        data = client.recv(1024)
        message = json.loads(data.decode())
        if message["type"] == "match_start":
            print(f"Match started! You are player {message['player_id']}.")
            return message['player_id']