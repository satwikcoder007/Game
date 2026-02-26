class Match:
    def __init__(self, p1, p2):
        self.players = [p1, p2]

    def broadcast(self, sender, data):
        for p in self.players:
            if p != sender:
                p.send(data)