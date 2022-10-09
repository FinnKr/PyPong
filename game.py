# -----imports-----
import pygame
import time
from pygame import mixer
from os.path import exists

# ---Global variables---


from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-W", "--width", dest="width", type=int, metavar="WIDTH", help="Set window width", default=800)
parser.add_argument("-H", "--height", dest="height", type=int, metavar="HEIGHT", help="Set window height", default=400)
parser.add_argument("-fps", "--framerate", dest="framerate", type=int, metavar="FRAMERATE",
                    help="Set desired framerate", default=60)
parser.add_argument("-fc", "--flipcolors", dest="fc", action="store_true", help="Flip black and white for another look of the game")
parser.add_argument("-sc", "--setcolor", dest="setcolors", type=int, default=0, help="Set color scheme using predefined setups. Values go from 0 to 5.")
parser.set_defaults(fc=False)

args = parser.parse_args()

screenWidth = args.width
screenHeight = args.height
FPS = args.framerate
flipcolors = args.fc
setcolors = args.setcolors

goals = [0, 0]

# colors
ownYellow = (230, 255, 0)
ownDarkBlue = (0, 10, 130)
ownBlue = (0,0,255)
ownMagenta = (199, 18, 145)
ownGreen = (0,255,0)
ownOrange = (255, 94, 0)
ownBlack = (0,0,0)
ownWhite = (255,255,255)
ownRed = (255,0,0)

colorSchemes = {
    0: {
        "first": ownBlack,
        "second": ownWhite
    },
    1: {
        "first": ownWhite,
        "second": ownBlack
    },
    2: {
        "first": ownBlack,
        "second": ownYellow
    },
    3: {
        "first": ownBlack,
        "second": ownRed
    },
    4: {
        "first": ownBlack,
        "second": ownBlue
    },
    5: {
        "first": ownBlack,
        "second": ownGreen
    }
}


# flip black and white if the flipcolors option is set
if(flipcolors):
    setcolors = 1

firstColor = colorSchemes[setcolors]["first"]
secondColor = colorSchemes[setcolors]["second"]

# -----Initializing the game-------
def init():
    pygame.init()  # initialize pygame module
    logo = pygame.image.load("resources/logo32x32.png")  # Load logo
    pygame.display.set_icon(logo)  # Set logo
    pygame.display.set_caption("Pong")  # Set window Title
    screen = pygame.display.set_mode(
        (screenWidth, screenHeight))  # Surface on screen with size of screenWidth x screenHeight
    screen.fill(firstColor)
    settings(screen)


# -----Settings-----
def settings(screen):
    font = pygame.font.SysFont("arialroundedmtbold", 24)
    settingsText = font.render("Settings", True, secondColor)
    screen.blit(settingsText, (screenWidth // 2 - settingsText.get_width() // 2, 10))
    pygame.display.flip()

    done = False
    startgame = False

    settingsList = [
        "Initial speed of the ball",
        "Number of players",
        "Moving speed of the players",
        "Ball size",
        "Paddle Length",
        "DONE"
    ]
    settingsIterator = 0
    settingsLength = len(settingsList)

    playerSpeed = 10  # Pixels the player moves per frame (speed)
    ballSpeed = 4  # "Speed" of the ball
    ballSize = 1
    playerNumber = 1
    paddleLength = 1
    lengthText = ["Short    ", "Normal", "Long     "] # Extra whitespace is to clear background when text changes


    renderAndUpdate(screen, str(ballSpeed), secondColor, firstColor,
                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(playerNumber), secondColor, firstColor,
                    (screenWidth // 2, 40 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(playerSpeed), secondColor, firstColor,
                    (screenWidth // 2, 60 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(ballSize), secondColor, firstColor,
                    (screenWidth // 2, 80 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(lengthText[paddleLength]), secondColor, firstColor,
                    (screenWidth // 2, 100 + 20 * settingsIterator + settingsText.get_height()))

    while not done:
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Event type = quit:
                done = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                settingsIterator += 1
                # resetting settingsIterator to 0 if it would be higher than any index of a setting in the list
                if settingsIterator == settingsLength:
                    settingsIterator = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                settingsIterator -= 1
                # resetting settingsIterator to last index of the settingsList if it would be lower than 0
                if settingsIterator == -1:
                    settingsIterator = settingsLength - 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                # determining which setting is selected and increasing (or decreasing value of that setting)
                if settingsIterator == 0:
                    ballSpeed += 1
                    renderAndUpdate(screen, str(ballSpeed), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 1:
                    if playerNumber == 1:
                        playerNumber = 2
                    else:
                        playerNumber = 1
                    renderAndUpdate(screen, str(playerNumber), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 2:
                    playerSpeed += 1
                    renderAndUpdate(screen, str(playerSpeed), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 3:
                    if (ballSize < 10):
                        ballSize += 1
                    renderAndUpdate(screen, str(ballSize), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 4:
                    paddleLength += 1
                    if (paddleLength > 2):
                        paddleLength = 0
                    renderAndUpdate(screen, str(lengthText[paddleLength]), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if settingsIterator == 0:
                    ballSpeed -= 1
                    if ballSpeed == 0:
                        ballSpeed = 1
                    renderAndUpdate(screen, str(ballSpeed), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 1:
                    if playerNumber == 1:
                        playerNumber = 2
                    else:
                        playerNumber = 1
                    renderAndUpdate(screen, str(playerNumber), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 2:
                    playerSpeed -= 1
                    if playerSpeed == 0:
                        playerSpeed = 1
                    renderAndUpdate(screen, str(playerSpeed), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 3:
                    if (ballSize > 1):
                        ballSize -= 1
                    renderAndUpdate(screen, str(ballSize), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 4:
                    paddleLength -= 1
                    if (paddleLength < 0):
                        paddleLength = 2
                    renderAndUpdate(screen, str(lengthText[paddleLength]), secondColor, firstColor,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))

            # if option "done" is selected and the return key is pressed the main function is called
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if settingsIterator == settingsLength - 1: # True on the last setting in the list
                    done = True
                    startgame = True

        # rendering the (selected) settings
        for i in range(settingsLength):
            if i == settingsIterator:
                setText = font.render(settingsList[i], True, firstColor, secondColor)
                screen.blit(setText, (10, 20 + 20 * i + setText.get_height()))
                pygame.display.flip()
            else:
                setText = font.render(settingsList[i], True, secondColor, firstColor)
                screen.blit(setText, (10, 20 + 20 * i + setText.get_height()))
                pygame.display.flip()

    if startgame:
        if exists('resources/gamemusic.mp3'):
            pygame.mixer.init()
            playerMusic = pygame.mixer.music.load('resources/gamemusic.mp3')
            pygame.mixer.music.play(-1)
        screen.fill(firstColor)
        main(screen, playerNumber, ballSpeed, playerSpeed, ballSize, paddleLength)


# -----Updating display with a text-----
def renderAndUpdate(screen, text, textColor, backgroundColor, pos):
    font = pygame.font.SysFont("arialroundedmtbold", 24)
    if len(text) == 2:
        text += "  "
    elif len(text) == 1:
        text += "   "
    valueText = font.render(text, True, textColor, backgroundColor)
    screen.blit(valueText, pos)
    pygame.display.flip()


# -----Update positions----- 
def updatePos(xPos, yPos, oldRect, screen, image):
    screen.fill(firstColor)
    updatedRect = screen.blit(image, (xPos, yPos))
    font = pygame.font.SysFont("arialroundedmtbold", 18)
    goalText = font.render(str(goals[0]) + " : " + str(goals[1]), True, secondColor, firstColor)
    pygame.display.update(updatedRect)
    pygame.display.update(oldRect)
    pygame.display.update(screen.blit(goalText, (screenWidth // 2 - goalText.get_width() // 2, 10)))
    return updatedRect


# -----Main function--------------
def main(screen, playerCount, ballSpeed, playerSpeed, ballSize, paddleLength):
    clock = pygame.time.Clock()

    xstepB = ballSpeed
    ystepB = ballSpeed
    running = True  # Variable for main loop control

    playerImg = pygame.image.load("resources/player.png")  # Load the player image
    playerImg = pygame.transform.scale(playerImg, (playerImg.get_size()[0],
                                       (int) (playerImg.get_size()[1] * [0.66, 1.0, 1.5][paddleLength]))) # Set the paddle length
    ballImg = pygame.image.load("resources/ball.png")
    ballImg = pygame.transform.scale(ballImg, [x * ballSize for x in ballImg.get_size()]) # Set the ball size

    screen.fill(firstColor)  # Fill the background with one colour (black)

    playerWidth = playerImg.get_width()  # Width of the player
    playerHeight = playerImg.get_height()  # Height of the player
    xpos1 = 20  # X-Position of the player 1
    xpos2 = screenWidth - 20 - playerWidth  # X-Position of the player 2
    ypos1 = screenHeight // 2 - playerHeight // 2  # Y-Position of the player 1
    ypos2 = ypos1  # Y-Position of the player 2

    ballWidth = ballImg.get_width()  # Width of the ball
    ballHeight = ballImg.get_height()  # Height of the ball
    xposB = xpos1 + playerWidth + 10  # X-Position of the ball
    yposB = ypos1 + playerHeight // 2 - ballHeight // 2  # Y-Position of the ball

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
        clock.tick(FPS)

        if not firstStart:

            # somebody scored
            if (xposB >= screenWidth) or (xposB <= 0):
                firstStart = True
                if xposB >= screenWidth:
                    goals[0] += 1
                else:
                    goals[1] += 1

                # resetting ball position
                xposB = screenWidth // 2 - ballWidth // 2 - xstepB
                yposB = screenHeight // 2 - ballHeight // 2 - ystepB

                # resetting speed of the ball
                xstepB = ballSpeed
                ystepB = ballSpeed

            # reversing ball if its out of the window (top or bottom)
            if (yposB + ballHeight >= screenHeight) or (yposB <= 0): 
                ystepB = -ystepB

            # Collision check with player 1
            # if ball with speed would be left of player 1
            if xposB - abs(xstepB) <= (xpos1 + playerWidth):
                # upDist = abs(yposB + ballHeight - ypos1)
                # downDist = abs(yposB - ypos1 - playerHeight)
                ystepBAbs = abs(ystepB)

                if (xposB - xstepB - 3 <= (xpos1 + playerWidth) and (
                        yposB + ballHeight >= ypos1 and yposB <= ypos1 + playerHeight)):
                    # Ball entered through top or bottom and is still inside the paddle
                    ystepB = +ystepBAbs
                elif (yposB + ballHeight > ypos1) and (yposB < ypos1 + playerHeight):
                    xAccelerator = 1 if xstepB > 1 else -1
                    xstepB = (-xstepB - xAccelerator)
                    yAccelerator = 1 if ystepB > 1 else -1
                    ystepB += yAccelerator

            # Collision check with player 2
            # if ball with speed is right to player 2
            if (xposB + ballWidth) + abs(xstepB) >= xpos2:

                # upDist = abs(yposB + ballHeight - ypos2)
                # downDist = abs(yposB - ypos2 - playerHeight)
                ystepBAbs = abs(ystepB)

                if (xposB + ballWidth - xstepB + 3 >= xpos2) and (
                        yposB + ballHeight >= ypos2 and yposB <= ypos2 + playerHeight):
                    # Ball entered through top or bottom and is still inside the paddle
                    ystepB = +ystepBAbs

                elif (yposB + ballHeight > ypos2) and (yposB < ypos2 + playerHeight):
                    xAccelerator = 1 if xstepB > 1 else -1
                    xstepB = (-xstepB - xAccelerator)
                    yAccelerator = 1 if ystepB > 1 else -1
                    ystepB += yAccelerator

            xposB += xstepB
            yposB += ystepB
            curRects[2] = updatePos(xposB, yposB, lastRects[2], screen, ballImg)
            lastRects[2] = curRects[2]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Event type = quit:
                running = False  # Change running to False -> Main loop quits

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

            # --- Bot for one player gaming --- #
        if playerCount == 1:
            if yposB > ypos2 + playerSpeed and ypos2 <= screenHeight - playerSpeed - playerHeight:
                # upPressed = False
                # downPressed = True
                ypos2 += playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]
            elif yposB < ypos2 - playerSpeed and ypos2 >= playerSpeed - playerHeight:
                # downPressed = False
                # upPressed = True
                ypos2 -= playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]

        # Actually moves the players if a key is pressed
        # First player
        if sPressed and ypos1 <= screenHeight - playerSpeed - playerHeight:
            ypos1 += playerSpeed
            curRects[0] = updatePos(xpos1, ypos1, lastRects[0], screen, playerImg)
            lastRects[0] = curRects[0]
        if wPressed and ypos1 >= playerSpeed:
            ypos1 -= playerSpeed
            curRects[0] = updatePos(xpos1, ypos1, lastRects[0], screen, playerImg)
            lastRects[0] = curRects[0]

            # Second player
        if playerCount == 2:
            if downPressed and ypos2 <= screenHeight - playerSpeed - playerHeight:
                ypos2 += playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]
            if upPressed and ypos2 >= playerSpeed:
                ypos2 -= playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]


if __name__ == "__main__":  # Only if the script is called as main script not if its imported as a module
    init()  # Call init function
