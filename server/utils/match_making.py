
from utils.match import Match

def match_making(lobby,matches,player_to_match):
    while len(lobby) >= 2: 
        player1 = lobby.pop(0) 
        player2 = lobby.pop(0) 
        match = Match(player1, player2)
        matches.append(match)
        player_to_match[player1] = match
        player_to_match[player2] = match
        print(f"Matched players {player1.getpeername()} and {player2.getpeername()}. Total matches: {len(matches)}")
        