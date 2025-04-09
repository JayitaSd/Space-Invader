import pygame
import random
import math
#from pygame.examples.video import backgrounds
from pygame import mixer

#initializing pygame to access all methods in the pygame module
pygame.init()
#create screen
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load('background.png')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1) #for looping


#change of title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#spaceship position
player_image = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

#enemy position
enemy_image = []
enemyX = []
enemyY=[]
enemyX_change=[]
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)


#bullet position
#ready - cant see the bullet on the screen
#fire- bullet is currently moving
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#positioning
textX = 10
textY=10

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

#function for displaying score
def showscore(x, y):
    score = font.render("Score: "+str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

#function for displaying game over
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_image,(x,y)) # requires 2 parameters(image,coordinates) and help draw image

def enemy(x, y, i):
    screen.blit(enemy_image[i],(x,y)) # requires 2 parameters(image,coordinates) and help draw image

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance<27:
        return True
    else:
        return False


#game loop
running = True
while running:

    # RGB background color
    screen.fill((0, 0, 0))  # only this won't work because we need to update it in the while loop

    #back img(to not disappear the back)
    screen.blit(background, (0,0)) #initialize to left corner

    #playerX -= 0.1 #maintaing the speed


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #if any keystroke is pressed check
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #checking if left key is pressed
                playerX_change=-5
            if event.key == pygame.K_RIGHT: #checking if right key is pressed
                playerX_change=5


            if event.key == pygame.K_SPACE: #checking if space key is pressed
                if bullet_state == "ready":

                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    #saves the initial firing coordinate
                    bulletX=playerX
                    fire_bullet(bulletX, bulletY)

        # release of keystroke
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change=0

#boundary for spaceship
    playerX += playerX_change

    if playerX<=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

#movement for enemies
    for i in range(num_of_enemies):

        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:

            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

            # reset the bullet position
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    #bullet initialisation
    if bulletY<=0:
        bulletY = 480
        bullet_state = "ready"
    #bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    showscore(textX, textY)

    pygame.display.update() #updating the color of the screen again and again

#1.44.48