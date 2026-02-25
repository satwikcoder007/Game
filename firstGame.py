from turtle import right

import pygame

pygame.init()

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
        self.walkFrame = 0
        self.ammo = 10
        self.max_ammo = 10
        self.last_reload_time = pygame.time.get_ticks()
        self.reload_delay = 5000
        self.walkRight = [pygame.image.load(f"assets/player{self.id}/R{i}.png") for i in range(1,10)]
        self.walkLeft = [pygame.image.load(f"assets/player{self.id}/L{i}.png") for i in range(1,10)]
        self.char = pygame.image.load(f"assets/player{self.id}/standing.png").convert_alpha()
        self.char = pygame.transform.scale(self.char, (self.width, self.height))
    def draw(self, win):
        if self.walkFrame > 17:
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
            self.ammo += 5
            self.ammo = min(self.ammo, self.max_ammo)
            self.last_reload_time = current_time
    def shoot(self):
        if self.ammo <= 0:
            return
        if self.right:
            facing = 1
        elif self.left:
            facing = 2
        elif self.up:
            facing = 3
        elif self.down:
            facing = 4
        else :
            facing = 1
        bullet = Projectile(self.id,self.x+self.width//2,self.y+self.height//2,5,(0,0,0),facing,8)
        bullets.append(bullet)
        self.ammo -= 1
        
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


def draw_ammo_segments(win, x, y, ammo, max_ammo, size=15, gap=3):
    for i in range(max_ammo):
        color = (50, 150, 255) if i < ammo else (60, 60, 60)
        pygame.draw.rect(win, color, (x + i*(size+gap), y, size, size))
        pygame.draw.rect(win, (255, 255, 255), (x + i*(size+gap), y, size, size), 1)
def redrawGameWindow():
    win.blit(bg, (0, 0))
    
    for player in players:
        player.draw(win)
        pygame.draw.rect(win, (255, 0, 0), (player.x, player.y, player.width, player.height), 2)
        if player.id == 1:
            draw_ammo_segments(win, 10, 10, player.ammo, player.max_ammo)
        else:
            draw_ammo_segments(win, length - 10 - player.max_ammo*18, 10, player.ammo, player.max_ammo)

    for bullet in bullets[:]:  # Iterate over a copy of the list to avoid modification issues 
        bullet.update()

        if bullet.is_on_screen(length, width):
            bullet.draw(win)
        else:
            bullets.remove(bullet)

    pygame.display.update()


players = [Player(1, 50, 410, 64, 64, 5, 10), Player(2, 400, 410, 69, 69, 5, 10)]

running = True
bullets = []

## This is the main game loop. It will run until the user closes the window. The loop checks for events (like key presses or mouse clicks) and updates the game state accordingly. In this case, we are only checking for the QUIT event, which is triggered when the user clicks the close button on the window. If that event is detected, we set running to False, which will exit the loop and end the game.
while running:
    clock.tick(27) ## This line sets the fps

    current_time = pygame.time.get_ticks()

    ## ammo refill
    for player in players:
        player.reload()

    keys = pygame.key.get_pressed() ## this line checks which keys are currently pressed and returns a list of boolean value

    for event in pygame.event.get(): ## This line retrives all the event object that occcured since the last time this line was executed.
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: ## this line checks if the right mouse button is pressed
            players[0].shoot()
    
    
    
    ## Horizontal movement
    if keys[pygame.K_a] and players[0].x>players[0].vel:
       players[0].x-=players[0].vel
       players[0].left = True
       players[0].right = False
       players[0].up = False
       players[0].down = False
    elif keys[pygame.K_d] and players[0].x<length-players[0].width-players[0].vel:
        players[0].x+=players[0].vel
        players[0].left = False
        players[0].right = True
        players[0].up = False
        players[0].down = False
    
    ## Vertical shooting movement
    elif keys[pygame.K_w]:
        players[0].left = False
        players[0].right = False
        players[0].up = True
        players[0].walkFrame = 0 
    elif keys[pygame.K_s]:
        players[0].left = False
        players[0].right = False
        players[0].up = False
        players[0].down = True
        players[0].walkFrame = 0
    else:
        players[0].walkFrame = 0
        
    ## Vertical movement (jumping) 
    if not players[0].isJump:
        if keys[pygame.K_SPACE]:
            players[0].isJump = True
            players[0].walkFrame = 0 
    else:
        players[0].jump()
    
    redrawGameWindow()

pygame.quit()
