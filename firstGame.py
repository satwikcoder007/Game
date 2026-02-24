from turtle import right

import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))
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


class player():
    def __init__(self, x, y, width, height,vel,jumpFrame):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.isJump = False
        self.jumpFrame = jumpFrame
        self.left = False
        self.right = False
        self.walkFrame = 0

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



man = player(50, 410, 64, 64, 5, 10)
running = True

def redrawGameWindow(man):
    win.blit(bg, (0, 0)) 
    man.draw(win)
    pygame.display.update() 
    
## This is the main game loop. It will run until the user closes the window. The loop checks for events (like key presses or mouse clicks) and updates the game state accordingly. In this case, we are only checking for the QUIT event, which is triggered when the user clicks the close button on the window. If that event is detected, we set running to False, which will exit the loop and end the game.
while running:
    clock.tick(27) ## This line sets the fps
    for event in pygame.event.get(): ## This line retrives all the event object that occcured since the last time this line was executed.
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed() ## this line checks which keys are currently pressed and returns a list of boolean value
    if keys[pygame.K_a] and man.x>man.vel:
       man.x-=man.vel
       man.left = True
       man.right = False
    elif keys[pygame.K_d] and man.x<500-man.width-man.vel:
        man.x+=man.vel
        man.left = False
        man.right = True
    else:
        man.left = False
        man.right = False
        man.walkFrame = 0 

    
    if not man.isJump:
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkFrame = 0 

    else:
        if man.jumpFrame >= -10:
            direction = 1
            if man.jumpFrame < 0:
                direction = -1
            man.y -= direction * (man.jumpFrame ** 2)*0.3
            man.jumpFrame -= 1
        else:
            man.isJump = False
            man.jumpFrame = 10
    redrawGameWindow(man)

pygame.quit()
