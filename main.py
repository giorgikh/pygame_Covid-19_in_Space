#!/usr/bin/python3
import pygame
import random
import math
import os
import sys
from pygame import mixer

global number_of_virus
global level

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('/home/giorgi/projects/pygame_projects/Space_Game/background.png')
pygame.display.set_caption("CoronaVirus in Space")
icon = pygame.image.load('/home/giorgi/projects/pygame_projects/Space_Game/icon.png')
pygame.display.set_icon(icon)

# player
player_image = pygame.image.load('/home/giorgi/projects/pygame_projects/Space_Game/spaceship.png')
playerX = 370
playerY = 530
playerX_change = 0
playerY_change = 0
exit_status = True

# virus
virus_image = []
virusX = []
virusY = []
virusX_change = []
virusY_change = []
number_of_virus = 7

for i in range(30):
    virus_image.append(pygame.image.load('/home/giorgi/projects/pygame_projects/Space_Game/virus.png'))
    virusX.append(random.randint(0, 730))
    virusY.append(random.randint(0, 330))
    virusX_change.append(10)
    virusY_change.append(40)

# bullet
# state :
# Ready - hided
# Fire - moving
bullet_image = pygame.image.load('/home/giorgi/projects/pygame_projects/Space_Game/bullet.png')
bulletX = 0
bulletY = 530
bulletY_change = 20
bullet_state = "ready"

# game over
game_over_font = pygame.font.Font('/home/giorgi/projects/pygame_projects/Space_Game/bpg_glaho_sylfaen.ttf', 48)

# score
score = 0
font = pygame.font.Font('/home/giorgi/projects/pygame_projects/Space_Game/bpg_glaho_sylfaen.ttf', 26)
textX = 10
textY = 10
level = 1

# background sound
mixer.music.load('/home/giorgi/projects/pygame_projects/Space_Game/background.wav')
mixer.music.play(-1)

restart_status = False


def game_over():
    text = game_over_font.render("თამაში დასრულდა", True, (0, 255, 0))
    screen.blit(text, (220, 300))


def show_restart():
    restart_click = font.render("რესტარტისთვის დააწექით Escape-ს", True, (0, 255, 0))
    screen.blit(restart_click, (250, 350))


def show_level():
    leve_value = font.render("დონე :" + str(level), True, (0, 255, 0))
    screen.blit(leve_value, (10, 40))


def restart():
    arguments = list(sys.argv)
    arguments.insert(0, sys.executable)
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    os.execv(__file__, sys.argv)


def show_score(textX, textY):
    score_value = font.render("ქულა : " + str(score), True, (0, 255, 0))
    screen.blit(score_value, (textX, textY))


def virus(x, y, i):
    screen.blit(virus_image[i], (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 19, y + 10))


def isCollision(virusX, virusY, bulletX, bulletY):
    distance = math.sqrt((math.pow(virusX - bulletX, 2)) + (math.pow((virusY - bulletY), 2)))
    if distance < 35:
        return True
    else:
        return False


while exit_status:
    screen.fill((96, 96, 96))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_status = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = - 5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_ESCAPE:

                if restart_status:
                    print(os.path.abspath(__file__))
                    restart()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    playerX += playerX_change
    playerY += playerY_change

    # player
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY < 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    for i in range(number_of_virus):
        if virusY[i] > 490:
            for k in range(number_of_virus):
                virusY[k] = 2000
            game_over()
            mixer.music.stop()
            show_restart()
            restart_status = True
            break
        # virus
        virusX[i] += virusX_change[i]
        if virusX[i] < 0:
            virusX[i] = 7536
            virusX_change[i] = -5
            virusY[i] += virusY_change[i]
        if virusX[i] >= 736:
            virusX[i] = 0
            virusX_change[i] = 5
            virusY[i] += virusY_change[i]
        player_coll = isCollision(virusX[i], virusY[i], playerX, playerY)
        if player_coll:
            for k in range(number_of_virus):
                virusY[k] = 2000
            game_over()
            player(370, 530)
            mixer.music.stop()
            show_restart()
            restart_status = True
            break

        # collision
        collision = isCollision(virusX[i], virusY[i], bulletX, bulletY)
        if collision:
            print("collision------", collision)
            bulletY = playerY
            bullet_state = "ready"
            score += 10
            virusY[i] = random.randint(0, 330)
            virusX[i] = random.randint(0, 730)
            print(score)
            if score > 300 and score < 600:
                number_of_virus = 10
                level = 2
            elif score > 600 and score < 900:
                number_of_virus = 15
                level = 3
            elif score > 900:
                number_of_virus = 20
                level = 4
            elif score > 900 and score < 1200:
                number_of_virus = 25
                level = 5

            elif score > 1200:
                number_of_virus = 30
                level = 6
        virus(virusX[i], virusY[i], i)
    # bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_level()
    pygame.display.flip()
    pygame.display.update()
