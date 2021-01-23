import pygame
import random
import math
from pygame import mixer

"""Be sure to check out file SpecialThanks.txt!"""

# init pygame
pygame.init()

# init game window
screen = pygame.display.set_mode((800, 600))

# title, icon, bacground
pygame.display.set_caption('SpaceInvaders Old Lawrence Odyssey 2021')
icon = pygame.image.load('img\\milky-way.png')
pygame.display.set_icon(icon)
background = pygame.image.load('img\\galaxy-4799471_1280.jpg')

# Bacground sound
mixer.music.load('ambient\\Jasper_-_Wobbly_Bass5.mp3')
mixer.music.play(-1)

# score
score_val = 0
font = pygame.font.Font('font\\ka1.ttf', 32)
textX = 12
textY = 12

# Game Over text
over_font = pygame.font.Font('font\\ka1.ttf', 72)
devilDoggy = pygame.image.load('img\\devil.png')

# insert Player - basic parameters
playerImg = pygame.image.load('img\\pervert.png')
playerX = 400 - 32
playerY = 600 - 64 - 25
playerX_avb = 0.4
playerX_change = 0

# increasing difficulties lvl
dif_lvl = 1

# insert Enemy - basic parameters
num_of_enemies = 3
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyX_inc = dif_lvl * 0.03
enemyY_inc = 0

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img\\enemy.png'))
    enemyX.append(random.randint(50, 750))
    enemyY.append(70)
    enemyX_change.append(dif_lvl * 0.25)
    enemyY_change.append(64 + 2)

# insert torpedooo!
torpedoImg = pygame.image.load('img\\torpedo.png')
torpedoX = playerX + 16
torpedoY = playerY - 16 - 2
torpedoX_change = 0
# 'ready' - you can shoot
# 'overload' - you can't shoot
torpedo_state = 'ready'
torpedoY_change = 0.05
torpedoY_inc = 0.002 / dif_lvl**2

def show_score(x, y):
    score = font.render('Your score: ' + str(score_val), True, (253, 66, 62))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (253, 66, 62))
    screen.blit(over_text, (130, 250))
    screen.blit(devilDoggy, (240, 450))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_torpedo(x, y):
    global torpedo_state
    torpedo_state = 'overload'
    screen.blit(torpedoImg, (x, y))

def aimedHit(enemyX, enemyY, torpedoX, torpedoY):
    distance = math.sqrt(((enemyX - torpedoX)**2) + ((enemyY - torpedoY)**2))
    if distance < 27:
        return True

# main dish
running = True
while running:

    # update  bacground color RGB
    screen.fill((14, 42, 112))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -playerX_avb
            if event.key == pygame.K_RIGHT:
                playerX_change = playerX_avb
            if event.key == pygame.K_SPACE:
                if torpedo_state == 'ready':
                    torpedo_Sound = mixer.Sound('ambient\\lock-load-silencer-gun-shot.wav')
                    torpedo_Sound.play()
                    torpedoX = playerX
                    fire_torpedo(torpedoX, torpedoY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # inserting a playera
    player(playerX, playerY)

    # torpedo run!
    if torpedoY <= 0:
        torpedoY = playerY - 16 - 2
        torpedo_state = 'ready'
        torpedoY_change = 0.05

    if torpedo_state == 'overload':
        fire_torpedo(torpedoX, torpedoY)
        torpedoY -= torpedoY_change
        torpedoY_change += torpedoY_inc

    # next player move
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 800 - 64:
        playerX = 800 - 64

    # next enemy move
    for i in range (num_of_enemies):

        # Game Over
        if enemyY[i] > 420:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 800 - 64:
            enemyX_change[i] = -enemyX_change[i] - enemyX_inc
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = abs(enemyX_change[i]) + enemyX_inc
            enemyY[i] += enemyY_change[i]

        # hit shoot!
        if aimedHit(enemyX[i], enemyY[i], torpedoX, torpedoY):
            wilhelm_Sound = mixer.Sound('ambient\\Wilhelm_Scream.ogg')
            wilhelm_Sound.play()
            torpedoY = playerY - 16 - 2
            torpedo_state = 'ready'
            torpedoY_change = 0.05
            score_val += 50
            # extra points for last line
            if enemyY[i] == 70:
                score_val += 25
            enemyX[i] = random.randint(50, 750)
            enemyY[i] = 70
            dif_lvl += 0.1

        enemy(enemyX[i], enemyY[i], i)

    # update screen inside loop
    show_score(textX, textY)
    pygame.display.update()

