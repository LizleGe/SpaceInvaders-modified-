import math
import random
import pygame
from pygame import mixer

pygame.init()  # The game is started

screen = pygame.display.set_mode((800, 600))  # The screen is created

background = pygame.image.load("background.png")  # The background image is loaded

mixer.music.load("spaceinvaders1.mpeg")  # The background music is loaded and looped
mixer.music.play(-1)

title = "Space Invaders"  # The title for Space Invaders
pygame.display.set_caption(title)
icon = pygame.image.load("mysterya.ico")  # The icon of the space invaders next to the caption.
pygame.display.set_icon(icon)


playerImg = pygame.image.load("player1.png")  # The player image is loaded
# The position/coordinates of the player
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6    # The number of the enemies

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load("saucer1b.ico"))  # picture of the enemy
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

laserImg = pygame.image.load("laser.png")  # The image of the laser that will be loaded
# The position of the missile
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = -1
laserState = "ready"


scoreValue = 0  # The value of the score
font = pygame.font.Font("freesansbold.ttf", 32)  # The font of the score
textX = 10  # The position of the score text
textY = 10

overFont = pygame.font.Font("freesansbold.ttf", 64)  # The game over text


def show_score(x, y):  # The player score is shown in the top left corner
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Show a big "GAME OVER" in the middle of the screen when the player loses
def game_over_text():
    overText = overFont.render("GAME OVER!", True, (255, 255, 255))  # When player looses
    screen.blit(overText, (200, 250))


def player(x, y):  # The position of the player is changed
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):  # The position of the enemy is changed
    screen.blit(enemyImg[i], (x, y))


def fire_laser(x, y):  # The missile is shown in front of the player spaceship
    global laserState
    laserState = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, laserX, laserY):   # The collision is detected between the enemy and the spacehip using the formula
    distance = math.sqrt(
        math.pow(enemyX - laserX, 2) + math.pow(enemyY - laserY, 2))

    if distance < 27:  # If the length between the enemy is less than 27 pixels, return to true if not False
        return True
    else:
        return False


running = True
while running:
    screen.fill((21, 21, 21))
    screen.blit(background, (0, 0))  # The display is shown

    for event in pygame.event.get():

        if event.type == pygame.QUIT:   # When the program is closed. The game will not loop.
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:  # If the ESC key is pressed, the game will quit.
                pygame.quit()

            if event.key == pygame.K_LEFT:  # If LEFT key is pressed player ship will move left.
                playerX_change = -0.7

            if event.key == pygame.K_RIGHT:  # If RIGHT key is pressed player ship will move right.
                playerX_change = 0.7

            if event.key == pygame.K_SPACE:  # When the SPACE key is pressed, the missile state is checked to see if ready.
                if laserState == "ready":

                    laserSound = mixer.Sound("laser.wav")  # laser sound is played
                    laserSound.play()

                    laserX = playerX  # The x coordinates of the missile is set to that of the spaceship

                    fire_laser(laserX, laserY)  # The missile is fired from the player's last know position.

        if event.type == pygame.KEYUP:  # When Up key is pressed look to see if its left or right

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # The movement of the player:

    playerX += playerX_change

    if playerX <= 0:  # When player is too far to the left its returned to play field.
        playerX = 0

    elif playerX >= 736:  # When player is too far to the right its returned to play field.
        playerX = 736

    for i in range(numOfEnemies):  # This is for each enemy

        if enemyY[i] > 440:  # The loop will be discontinued if the enemy is more than 440
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]  # This is the enemy movement. The enemy changes its x-position based on own x-change value

        if enemyX[i] <= 0:  # Current enemy position is less or equal to 0.
            enemyX_change[i] = 0.5  # Enemy will move to the right the whole time and move down slightly
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:  # Current enemy position is less or equal to 736
            enemyX_change[i] = -0.5  # Enemy will move to the left the whole time and move down slightly
            enemyY[i] += enemyY_change[i]

        if laserY <= -64:  # When the laser goes off the screen the y-position of the missile will be reset and chagne to ready.
            laserY = 480
            laserState = "ready"

        if laserState == "fire": # When the laser is fired, the function will be called, the y-value will be changed to y-change value.
            fire_laser(laserX, laserY)
            laserY += laserY_change

        collision = is_collision(enemyX[i], enemyY[i], laserX, laserY)   # Check for collision between enemy and the laser

        if collision:   # The explosion sound is played the missile is reset, increased and the score updated.
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            laserY = 480
            laserState = "ready"
            scoreValue += 1
            print(scoreValue)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)  # The current position of enemy is updated

    player(playerX, playerY)  # The player position is updated

    show_score(textX, textY)  # The current score is shown

    pygame.display.update()  # The screen is updated

