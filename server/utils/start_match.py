import json


def start_match(match):
    msg1 = json.dumps({"type": "match_start", "player_id": 1}).encode()
    msg2 = json.dumps({"type": "match_start", "player_id": 2}).encode()

    match.players[0].send(msg1)
    match.players[1].send(msg2)
    