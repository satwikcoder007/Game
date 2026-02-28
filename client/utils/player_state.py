def get_player_state(player):
    return {
        "x": player.x,
        "y": player.y,
        "left": player.left,
        "right": player.right,
        "up": player.up,
        "down": player.down,
        "moving": player.moving
    }

def set_player_state(player, state):
    player.x = state["x"]
    player.y = state["y"]
    player.left = state["left"]
    player.right = state["right"]
    player.up = state["up"]
    player.down = state["down"]
    player.moving = state["moving"]