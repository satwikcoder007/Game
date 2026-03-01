import pygame

from utils.send_message import send_message
from utils.player_state import get_player_state, set_player_state

pygame.init()
pygame.mixer.init()

length = 500
width = 480

win = pygame.display.set_mode((length, width))
"""
this is the window object that we will be using to display our game. The argument (500, 500) is the size of the window in pixels. 
The first number is the width and the second number is the height.
"""

pygame.display.set_caption("First Game")
clock = pygame.time.Clock()

bg = pygame.image.load('assets/bg.jpg')
font = pygame.font.SysFont("arial", 24)

## sound effects
shoot_sound = pygame.mixer.Sound("assets/sounds/impact.mp3")
shoot_sound.set_volume(0.4)

hurt_sound = pygame.mixer.Sound("assets/sounds/hurt.mp3")
hurt_sound.set_volume(0.4)

reload_sound = pygame.mixer.Sound("assets/sounds/reload.mp3")
reload_sound.set_volume(0.4)

victory_sound = pygame.mixer.Sound("assets/sounds/victory.mp3")
victory_sound.set_volume(0.4)

defeat_sound = pygame.mixer.Sound("assets/sounds/defeat.mp3")
defeat_sound.set_volume(0.4)

jump_sound = pygame.mixer.Sound("assets/sounds/jump.mp3")
jump_sound.set_volume(0.1)

class Player:

    def __init__(self, id, x, y, width, height,vel,jumpFrame):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.isJump = False
        self.jumpFrame = jumpFrame
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.moving = False
        self.walkFrame = 0
        self.ammo = 10
        self.max_ammo = 10
        self.health = 10
        self.max_health = 10    
        self.last_reload_time = pygame.time.get_ticks()
        self.reload_delay = 5000
        self.hitbox_width = 28
        self.hitbox_height = 60
        self.hitbox = self.update_hitbox()
        self.walkRight = [pygame.image.load(f"assets/player{self.id}/R{i}.png") for i in range(1,10)]
        self.walkLeft = [pygame.image.load(f"assets/player{self.id}/L{i}.png") for i in range(1,10)]
        self.char = pygame.image.load(f"assets/player{self.id}/standing.png") 
    def draw(self, win):
        if self.walkFrame > len(self.walkRight)*2 - 1 or self.moving == False:
            self.walkFrame = 0
        if self.right:
            win.blit(self.walkRight[self.walkFrame//2],(self.x,self.y))
            self.walkFrame += 1
        elif self.left:
            win.blit(self.walkLeft[self.walkFrame//2],(self.x,self.y))
            self.walkFrame += 1
        else:
            self.walkFrame = 0
            win.blit(self.char, (self.x, self.y))

        self.hitbox = self.update_hitbox()
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    def jump(self):
        if self.jumpFrame >= -10:
            direction = 1
            if self.jumpFrame < 0:
                direction = -1
            self.y -= direction * (self.jumpFrame ** 2)*0.3
            self.jumpFrame -= 1
        else:
            self.isJump = False
            self.jumpFrame = 10
    def reload(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_reload_time >= self.reload_delay:
            if self.ammo < self.max_ammo:
                reload_sound.play()
            self.ammo += 5
            self.ammo = min(self.ammo, self.max_ammo)
            self.last_reload_time = current_time
    def shoot(self):
        if self.ammo <= 0:
            return None
        if self.right:
            facing = 1
        elif self.left:
            facing = 2
        elif self.up:
            facing = 3
        elif self.down:
            facing = 4
        else :
            facing = 1 if self.id == 1 else 2
        bullet = Projectile(self.id,self.x+self.width//2,self.y+self.height//2,5,(0,0,0),facing,8)
        self.ammo -= 1
        return bullet
    def update_hitbox(self):
        if self.id == 1:

            return (
                self.x + self.width // 2 - self.hitbox_width // 2,  
                self.y + self.height - self.hitbox_height,          
                self.hitbox_width,
                self.hitbox_height
            )
        else:
            
           return (
                self.x,
                self.y,
                self.hitbox_width,
                self.hitbox_height
            )    
        
class Projectile:

    def __init__(self, id, x, y, radius, color, facing, vel):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = vel
    def update(self):
        if self.facing == 1:  
            self.x += self.vel
        elif self.facing == 2:  
            self.x -= self.vel
        elif self.facing == 3:  
            self.y -= self.vel
        else:  
            self.y += self.vel
    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
    def is_on_screen(self, width, height):
        return 0 < self.x < width and 0 < self.y < height

def draw_heart(win, x, y, size, color):
    r = size // 4
    pygame.draw.circle(win, color, (x + r, y + r), r)
    pygame.draw.circle(win, color, (x + 3*r, y + r), r)
    points = [
        (x, y + r),
        (x + size, y + r),
        (x + size//2, y + size)
    ]
    pygame.draw.polygon(win, color, points)
def draw_health_hearts(win, x, y, health, max_health, size=12, gap=6):
    for i in range(max_health):
        color = (220, 20, 60) if i < health else (80, 80, 80)
        draw_heart(win, x + i*(size + gap), y, size, color)
def draw_ammo_segments(win, x, y, ammo, max_ammo, size=15, gap=3):
    for i in range(max_ammo):
        color = (50, 150, 255) if i < ammo else (60, 60, 60)
        pygame.draw.rect(win, color, (x + i*(size+gap), y, size, size))
        pygame.draw.rect(win, (255, 255, 255), (x + i*(size+gap), y, size, size), 1)
def redrawGameWindow(players, bullets, player_id):
    opponent_id = 2 if player_id == 1 else 1
    win.blit(bg, (0, 0))
    
    for player in players:
        player.draw(win)
        if player.id == 1:
            draw_ammo_segments(win, 10, 10, player.ammo, player.max_ammo)
            draw_health_hearts(win, 10, 40, player.health, player.max_health)
        else:
            draw_ammo_segments(win, length - 10 - player.max_ammo*18, 10, player.ammo, player.max_ammo)
            draw_health_hearts(win, length - 10 - player.max_health*18, 40, player.health, player.max_health)

    for bullet in bullets[:]:  # Iterate over a copy of the list to avoid modification issues 
        bullet.update()
        if bullet.id == player_id and players[opponent_id-1].hitbox[0] < bullet.x < players[opponent_id-1].hitbox[0] + players[opponent_id-1].hitbox[2] and players[opponent_id-1].hitbox[1] < bullet.y < players[opponent_id-1].hitbox[1] + players[opponent_id-1].hitbox[3]:
            players[opponent_id-1].health -= 1
            bullets.remove(bullet)
            shoot_sound.play()
        if bullet.id == opponent_id and players[player_id-1].hitbox[0] < bullet.x < players[player_id-1].hitbox[0] + players[player_id-1].hitbox[2] and players[player_id-1].hitbox[1] < bullet.y < players[player_id-1].hitbox[1] + players[player_id-1].hitbox[3]:
            players[player_id-1].health -= 1
            bullets.remove(bullet)
            hurt_sound.play()
        if bullet.is_on_screen(length, width):
            bullet.draw(win)
        else:
            bullets.remove(bullet)

    pygame.display.update()


def run_game(client, player_id,opponent_queue):
    opponent_id = 2 if player_id == 1 else 1
    players = [Player(1, 50, 410, 64, 64, 4, 10), Player(2, 400, 410, 64, 64, 4, 10)]
    running = True
    bullets = []
    last_state = None
    ## This is the main game loop. It will run until the user closes the window. The loop checks for events (like key presses or mouse clicks) and updates the game state accordingly. In this case, we are only checking for the QUIT event, which is triggered when the user clicks the close button on the window. If that event is detected, we set running to False, which will exit the loop and end the game.
    while running:
        clock.tick(32) ## This line sets the fps

        ## Check for game over
        if players[player_id-1].health <= 0:
            send_message(client, {
                "type": "game_over",
                "winner": opponent_id
            })
            win.blit(bg, (0, 0))
            text = font.render("You Lose!", True, (255, 0, 0))
            win.blit(text, (length//2 - text.get_width()//2, width//2 - text.get_height()//2))
            pygame.display.update()
            defeat_sound.play()
            pygame.time.delay(5000)
            running = False
        ## ammo refill
        for player in players:
            player.reload()

        keys = pygame.key.get_pressed() ## this line checks which keys are currently pressed and returns a list of boolean value

        for event in pygame.event.get(): ## This line retrives all the event object that occcured since the last time this line was executed.
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: ## this line checks if the right mouse button is pressed
               bullet = players[player_id-1].shoot()
               if bullet:
                   send_message(client, {
                        "type": "shoot",
                        "id": bullet.id,
                        "x": bullet.x,
                        "y": bullet.y,
                        "radius": bullet.radius,
                        "color": bullet.color,
                        "facing": bullet.facing,
                        "vel": bullet.vel,
                        "ammo": players[player_id-1].ammo,
                   })
                   bullets.append(bullet)
        
        
        ## Horizontal movement
        if keys[pygame.K_a] and players[player_id-1].x>players[player_id-1].vel:
            players[player_id-1].x-=players[player_id-1].vel
            players[player_id-1].moving = True
            players[player_id-1].left = True
            players[player_id-1].right = False
            players[player_id-1].up = False
            players[player_id-1].down = False  
        elif keys[pygame.K_d] and players[player_id-1].x<length-players[player_id-1].width-players[player_id-1].vel:
            players[player_id-1].x+=players[player_id-1].vel
            players[player_id-1].moving = True
            players[player_id-1].left = False
            players[player_id-1].right = True
            players[player_id-1].up = False
            players[player_id-1].down = False
        
        ## Vertical shooting movement
        elif keys[pygame.K_w]:
            players[player_id-1].moving = False
            players[player_id-1].left = False
            players[player_id-1].right = False
            players[player_id-1].up = True
            players[player_id-1].down = False
        elif keys[pygame.K_s]:
            players[player_id-1].moving = False
            players[player_id-1].left = False
            players[player_id-1].right = False
            players[player_id-1].up = False
            players[player_id-1].down = True
        else:
            players[player_id-1].moving = False
            
        ## Vertical movement (jumping) 
        if not players[player_id-1].isJump:
            if keys[pygame.K_SPACE]:
                players[player_id-1].isJump = True
                jump_sound.play()
        else:
            players[player_id-1].jump()
        
        ## Send player state to server if changed
        current_state = get_player_state(players[player_id-1])
        if current_state != last_state:
            send_message(client, {
                "type": "move",
                **current_state
            })
            last_state = current_state
        
        ##update opponent state from server messages
        while not opponent_queue.empty():
            message = opponent_queue.get()
            if message["type"] == "move":
                opponent_state = {
                    "x": message["x"],
                    "y": message["y"],
                    "left": message["left"],
                    "right": message["right"],
                    "up": message["up"],
                    "down": message["down"],
                    "moving": message["moving"]
                }
                set_player_state(players[opponent_id-1], opponent_state)
            elif message["type"] == "shoot":
                bullet = Projectile(message["id"], message["x"], message["y"], message["radius"], message["color"], message["facing"], message["vel"])
                players[opponent_id-1].ammo = message["ammo"]
                bullets.append(bullet)
            else:
                win.blit(bg, (0, 0))
                text = font.render("You Win!", True, (255, 0, 0))
                win.blit(text, (length//2 - text.get_width()//2, width//2 - text.get_height()//2))
                pygame.display.update()
                victory_sound.play()
                pygame.time.delay(5000)
                running = False
        
        redrawGameWindow(players, bullets, player_id)

    pygame.quit()

