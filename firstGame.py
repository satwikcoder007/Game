import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))
"""
this is the window object that we will be using to display our game. The argument (500, 500) is the size of the window in pixels. 
The first number is the width and the second number is the height.
"""

pygame.display.set_caption("First Game")


walkRight = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walkLeft = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
char = pygame.image.load('assets/standing.png')

x = 50
y = 425
width = 64
height = 64
vel = 5

isJump = False
jumpFrame = 10
left = False
right = False
walkFrame = 0

running = True
## This is the main game loop. It will run until the user closes the window. The loop checks for events (like key presses or mouse clicks) and updates the game state accordingly. In this case, we are only checking for the QUIT event, which is triggered when the user clicks the close button on the window. If that event is detected, we set running to False, which will exit the loop and end the game.
while running:
    pygame.time.delay(100) 
    for event in pygame.event.get(): ## This line retrives all the event object that occcured since the last time this line was executed.
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed() ## this line checks which keys are currently pressed and returns a list of boolean value
    if keys[pygame.K_a] and x>vel:
       x-=vel
    if keys[pygame.K_d] and x<500-width-vel:
        x+=vel
    
    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpFrame >= -10:
            direction = 1
            if jumpFrame < 0:
                direction = -1
            y -= direction * (jumpFrame ** 2)*0.5
            jumpFrame -= 1
        else:
            isJump = False
            jumpFrame = 10

    win.fill((0, 0, 0)) ## This clears the previous frame 
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) ## This line draws a rectangle on the window.
    pygame.display.update() ## This line updates the display to show the changes we made to the window.

pygame.quit()
