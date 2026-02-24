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

walkRight = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')


class Player():
    def __init__(self, x, y, width, height,vel,jumpFrame):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.isJump = False
        self.jumpFrame = jumpFrame
        self.left = False
        self.right = True
        self.walkFrame = 0
        self.ammo = 10
        self.last_reload_time = pygame.time.get_ticks()
        self.reload_delay = 5000

    def draw(self, win):
        if self.walkFrame > 17:
            self.walkFrame = 0
        if self.right:
            win.blit(walkRight[self.walkFrame//2],(self.x,self.y))
            self.walkFrame += 1
        elif self.left:
            win.blit(walkLeft[self.walkFrame//2],(self.x,self.y))
            self.walkFrame += 1
        else:
            win.blit(char, (self.x, self.y))
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
            self.ammo = min(self.ammo, 10)
            self.last_reload_time = current_time
    def shoot(self):
        if self.ammo <= 0:
            return
        if self.right:
            facing = 1
        else:
            facing = -1
        bullet = Projectile(self.x+self.width//2,self.y+self.height//2,5,(0,0,0),facing,8)
        bullets.append(bullet)
        self.ammo -= 1
        
class Projectile:
    def __init__(self, x, y, radius, color, facing, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = vel

    def update(self):
        self.x += self.vel * self.facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def is_on_screen(self, width):
        return 0 < self.x < width




def redrawGameWindow(man):
    win.blit(bg, (0, 0))
    man.draw(win)

    for bullet in bullets[:]:  # Iterate over a copy of the list to avoid modification issues 
        bullet.update()

        if bullet.is_on_screen(length):
            bullet.draw(win)
        else:
            bullets.remove(bullet)

    pygame.display.update()

man = Player(50, 410, 64, 64, 5, 10)
running = True
bullets = []

## This is the main game loop. It will run until the user closes the window. The loop checks for events (like key presses or mouse clicks) and updates the game state accordingly. In this case, we are only checking for the QUIT event, which is triggered when the user clicks the close button on the window. If that event is detected, we set running to False, which will exit the loop and end the game.
while running:
    clock.tick(27) ## This line sets the fps

    current_time = pygame.time.get_ticks()

    ## ammo refill
    man.reload()

    for event in pygame.event.get(): ## This line retrives all the event object that occcured since the last time this line was executed.
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: ## this line checks if the right mouse button is pressed
            man.shoot()
    
    keys = pygame.key.get_pressed() ## this line checks which keys are currently pressed and returns a list of boolean value
    
    ## Horizontal movement
    if keys[pygame.K_a] and man.x>man.vel:
       man.x-=man.vel
       man.left = True
       man.right = False
    elif keys[pygame.K_d] and man.x<length-man.width-man.vel:
        man.x+=man.vel
        man.left = False
        man.right = True
    else:
        man.walkFrame = 0 
        
    ## Vertical movement (jumping) 
    if not man.isJump:
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkFrame = 0 
    else:
        man.jump()
    
    redrawGameWindow(man)

pygame.quit()
