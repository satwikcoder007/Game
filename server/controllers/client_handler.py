import select

def client_handler(match,matches,player_to_match):
    sockets = match.players  

    while True:
        try:
            readable, _, _ = select.select(sockets, [], []) ## Wait for any socket to be ready for reading

            for sock in readable:
                data = sock.recv(1024)

                ## empty read means other player terminated connection
                if not data:
                    print("Player disconnected")
                    match.close()
                    matches.remove(match)
                    del player_to_match[match.players[0]]
                    del player_to_match[match.players[1]]
                    return

                match.broadcast(sock, data)

        except Exception as e:
            print("Match error:", e)
            match.close()
            matches.remove(match)
            del player_to_match[match.players[0]]
            del player_to_match[match.players[1]]
            return