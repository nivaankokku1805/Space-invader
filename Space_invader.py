import pygame
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('bg.png')

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

player_img = pygame.image.load('player.png')
player_x = PLAYER_START_X
player_y = PLAYER_START_Y
playerX_change = 0

enemy_Img = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_Img.append(pygame.image.load('enemy.png'))
    enemy_X.append(random.randint(0, SCREEN_WIDTH - 64))
    enemy_Y.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)
    
bullet_Img = pygame.image.load('bullet.png')
bullet_X = 0
bullet_Y = PLAYER_START_Y
bulletX_change = 0 
bulletY_change = BULLET_SPEED_Y
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    
def player(x, y):
    screen.blit(player_Img, (x, y))
    
def enemy(x, y, i):
    screen.blit(enemy_Img[i], (x, y))
    
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) 
    return distance < COLLISION_DISTANCE      
        
        
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bullet_X = player_x
                    fire_bullet(bullet_X, bullet_Y)
                    
        if event.type == pygame.KEYUP and  event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
                
    playerX += playerX_change
    playerX = max(0,min(player_X, SCREEN_WIDTH - 64))
        
   
        
    for i in range(num_of_enemies):
        if enemy_Y[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
            
        enemy_X[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemy_X[i] >= SCREEN_WIDTH - 64:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
            
       
            
        if is_collision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y):
            bulletY = PLAYER_START_Y
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)
        enemy(enemy_X[i], enemy_Y[i], i)
        
    if bullet_Y <= 0:
        bullet_Y = PLAYER_START_Y
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bulletY_change
    
        
    player(player_x, player_y)
    show_score(textX, textY)
    pygame.display.update()