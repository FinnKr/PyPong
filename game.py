# -----imports-----
import pygame
import time

# ---Global variables---
screenWidth = 800
screenHeight = 400
goals = [0, 0]


# -----Player Select function-----
def playerselect(screen):
    font = pygame.font.SysFont("arialroundedmtbold", 18)
    textP1 = font.render("1 Player", True, (0, 0, 0), (255, 255, 255))
    textP2 = font.render("2 Player", True, (255, 255, 255), (0, 0, 0))
    screen.blit(textP1, (10, 10))
    screen.blit(textP2, (10, 10 + textP1.get_height() + 10))
    pygame.display.flip()

    selectedP = 1
    done = False
    startgame = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Event type = quit:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                done = True
                startgame = True
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                if selectedP == 1:
                    selectedP = 2
                    textP1 = font.render("1 Player", True, (255, 255, 255), (0, 0, 0))
                    textP2 = font.render("2 Player", True, (0, 0, 0), (255, 255, 255))
                elif selectedP == 2:
                    selectedP = 1
                    textP1 = font.render("1 Player", True, (0, 0, 0), (255, 255, 255))
                    textP2 = font.render("2 Player", True, (255, 255, 255), (0, 0, 0))
                screen.blit(textP1, (10, 10))
                screen.blit(textP2, (10, 10 + textP1.get_height() + 10))
                pygame.display.flip()
    if startgame:
        main(screen, selectedP)


# -----Initializing the game-------
def init():
    pygame.init()  # initialize pygame module
    logo = pygame.image.load("resources/logo32x32.png")  # Load logo
    pygame.display.set_icon(logo)  # Set logo
    pygame.display.set_caption("Pong")  # Set window Title
    screen = pygame.display.set_mode((screenWidth, screenHeight))  # Surface on screen with size 240x180
    playerselect(screen)


def updatePos(xPos, yPos, oldRect, screen, image):
    screen.fill((0, 0, 0))
    updatedRect = screen.blit(image, (xPos, yPos))
    font = pygame.font.SysFont("arialroundedmtbold", 18)
    goalText = font.render(str(goals[0]) + " : " + str(goals[1]), True, (255, 255, 255), (0, 0, 0))
    pygame.display.update(updatedRect)
    pygame.display.update(oldRect)
    pygame.display.update(screen.blit(goalText, (screenWidth / 2 - goalText.get_width() / 2, 10)))
    return updatedRect


# -----Main function--------------
def main(screen, playerCount):
    running = True  # Variable for main loop control

    playerImg = pygame.image.load("resources/player.png")  # Load the player image
    ballImg = pygame.image.load("resources/ball.png")

    screen.fill((0, 0, 0))  # Fill the background with one colour (black)

    playerWidth = playerImg.get_width()         # Width of the player
    playerHeight = playerImg.get_height()       # Height of the player
    xpos1 = 20                                  # X-Position of the player 1
    xpos2 = screenWidth - 20 - playerWidth      # X-Position of the player 2
    ypos1 = screenHeight / 2 - playerHeight / 2 # Y-Position of the player 1
    ypos2 = ypos1                               # Y-Position of the player 2
    stepP = 10                                  # Pixels the player moves per frame (speed)

    ballWidth = ballImg.get_width()  # Width of the ball
    ballHeight = ballImg.get_height()  # Height of the ball
    xposB = xpos1 + playerWidth + 10  # X-Position of the ball
    yposB = ypos1 + playerHeight / 2 - ballHeight / 2  # Y-Position of the ball
    xstepB = 4  # "Speed" of the ball
    ystepB = 4

    lastRects = [screen.blit(playerImg, (xpos1, ypos1)),  # Which parts of the screen
                 screen.blit(playerImg, (xpos2, ypos2)),  # needs to be updated
                 screen.blit(ballImg, (xposB, yposB))]

    curRects = lastRects.copy()

    pygame.display.flip()  # Refresh the screen

    firstStart = True
    upPressed = False
    downPressed = False
    wPressed = False
    sPressed = False

    # -----main loop-----
    while running:
        # ---event handling, gets all events from event queue---
        time.sleep(0.03)
        if not firstStart:
            if (xposB >= screenWidth) or (xposB <= 0):
                firstStart = True
                if (xposB >= screenWidth):
                    goals[0] += 1
                else:
                    goals[1] += 1
                xposB = screenWidth/2 - ballWidth/2 - xstepB
                yposB = screenHeight/2 - ballHeight/2 - ystepB
            if (yposB >= screenHeight) or (yposB <= 0):
                ystepB = -ystepB

            # Collision check with player 1
            if (xposB-3 <= (xpos1 + playerWidth)):

                if (yposB+ballHeight > ypos1) and (yposB < ypos1+playerHeight):
                    xAccelerator = 1 if xstepB > 1 else -1
                    xstepB = (-xstepB - xAccelerator)
            if ((xposB + ballWidth)+3 >= xpos2):
                if (yposB+ballHeight > ypos2) and (yposB < ypos2+playerHeight):
                    yAccelerator = 1 if ystepB > 1 else -1
                    xstepB = (-xstepB - yAccelerator)

                upDist = abs(yposB + ballHeight - ypos1)
                downDist = abs(yposB - ypos1 - playerHeight)
                ystepBAbs = abs(ystepB)
                
                if (xposB - xstepB - 3 <= (xpos1 + playerWidth) and (yposB + ballHeight >= ypos1 and yposB <= ypos1 + playerHeight)):
                    # Ball entered through top or bottom and is still inside the paddle
                    if (upDist < downDist):  # ball is above
                        ystepB = -ystepBAbs 
                    else: 
                        ystepB = +ystepBAbs
                elif (yposB+ballHeight > ypos1) and (yposB < ypos1+playerHeight):
                    xstepB = -xstepB

            # Collision check with player 2
            if ((xposB + ballWidth)+3 >= xpos2):
                upDist = abs(yposB + ballHeight - ypos2)
                downDist = abs(yposB - ypos2 - playerHeight)
                ystepBAbs = abs(ystepB)
                
                if (xposB + ballWidth - xstepB + 3 >= xpos2) and (yposB + ballHeight >= ypos2 and yposB <= ypos2 + playerHeight):
                    # Ball entered through top or bottom and is still inside the paddle
                    if (upDist < downDist):  # ball is above
                        ystepB = -ystepBAbs 
                    else: 
                        ystepB = +ystepBAbs

                elif (yposB+ballHeight > ypos2) and (yposB < ypos2+playerHeight):
                    xstepB = -xstepB
            
            xposB += xstepB
            yposB += ystepB
            curRects[2] = updatePos(xposB, yposB, lastRects[2], screen, ballImg)
            lastRects[2] = curRects[2]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Event type = quit:
                running = False             # Change running to False -> Main loop quits

            # Switches firstStart variable if the game is started
            if firstStart:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    firstStart = False
           
            # Switches the variables for the key pressed when they are pressed or released
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                downPressed = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                upPressed = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                sPressed = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                wPressed = True

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                downPressed = False
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                upPressed = False

            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                sPressed = False
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                wPressed = False

            # --- Bot for one player gamming --- #
        if playerCount == 1:
            if yposB + 1 + stepP > ypos2:
                #upPressed = False
                #downPressed = True
                ypos2 += stepP
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]
            if yposB - 1 - stepP < ypos2:
                #downPressed = False
                #upPressed = True
                ypos2 -= stepP
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]

        # Actually moves the players if a key is pressed
        # First player
        if sPressed and ypos1 <= screenHeight - stepP - (playerHeight//2):
            ypos1 += stepP
            curRects[0] = updatePos(xpos1, ypos1, lastRects[0], screen, playerImg)
            lastRects[0] = curRects[0]
        if wPressed and ypos1 >= 0 + stepP - (playerHeight//2):
            ypos1 -= stepP
            curRects[0] = updatePos(xpos1, ypos1, lastRects[0], screen, playerImg)
            lastRects[0] = curRects[0]    
        
        # Second player
        if playerCount == 2:
            if downPressed and ypos2 <= screenHeight - stepP - (playerHeight//2):
                ypos2 += stepP
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]
            if upPressed and ypos2 >= 0 + stepP - (playerHeight//2):
                ypos2 -= stepP
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]


if __name__ == "__main__":  # Only if the script is called as main script not if its imported as a module
    init()  # Call init function
