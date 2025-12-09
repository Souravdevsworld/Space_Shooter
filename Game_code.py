import math
from random import randint
import pygame
from pygame import mixer

#initialise the pygame
pygame.init()

# Initialize mixer for sound
pygame.mixer.init()

#create the screen 
screen = pygame.display.set_mode((800,600))

#Background 
background = pygame.image.load('bground.png')

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# caption and icon 
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player 
playerImg = pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0

# enemy alien
alienImg =[]
alienX=[]
alienY=[]
alienX_change=[]
alienY_change=[]
num_of_enemies = 6

for i in range(num_of_enemies):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(randint(0,735))
    alienY.append(randint(50,150))
    alienX_change.append(1)
    alienY_change.append(40)

#Bullets - Multiple bullets system
bulletImg = pygame.image.load('bullet.png')
bullets = []  # List to store all active bullets
bulletY_change = 2

# Sound effects
laser_sound = pygame.mixer.Sound('laser.wav')
collision_sound = pygame.mixer.Sound('explosion.wav')

#score
score_value = 0 
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Game Over 
over_font = pygame.font.Font('freesansbold.ttf',64)
game_over = False  # Add game over flag

# Track the last milestone reached for adding aliens
last_milestone = 0

def show_score(x,y):
    score = font.render("SCORE : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(playerImg,(x,y))

def alien(x,y,i):
    screen.blit(alienImg[i],(x,y))

def fire_bullet(x, y):
    """Create a new bullet at the given position"""
    bullet = {
        'x': x + 16,  # Center the bullet on the player
        'y': y + 10,
        'active': True
    }
    bullets.append(bullet)
    laser_sound.play()  # Play laser sound when bullet is fired

def update_bullets():
    """Update all bullet positions and remove inactive ones"""
    for bullet in bullets[:]:  # Use slice copy to safely modify list during iteration
        if bullet['active']:
            bullet['y'] -= bulletY_change
            # Remove bullet if it goes off screen
            if bullet['y'] <= 0:
                bullets.remove(bullet)
        else:
            bullets.remove(bullet)

def draw_bullets():
    """Draw all active bullets"""
    for bullet in bullets:
        if bullet['active']:
            screen.blit(bulletImg, (bullet['x'], bullet['y']))   

def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX-bulletX,2) + math.pow(alienY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

def add_aliens(count):
    """Add new aliens to the game"""
    global num_of_enemies
    for i in range(count):
        alienImg.append(pygame.image.load('alien.png'))
        alienX.append(randint(0,735))
        alienY.append(randint(50,150))
        alienX_change.append(1)
        alienY_change.append(40)
    num_of_enemies += count

# Game loop
running=True 
while running:
    
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if not game_over:  # Only fire if game is not over
                    fire_bullet(playerX, playerY)  

        if event.type==pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
    # Only update game if not game over
    if not game_over:
        #checking for boundaries of spaceship so it doesn't go out of boundary
        playerX  += playerX_change
        if playerX <=0 :
            playerX = 0
        elif playerX >= 736:
            playerX = 736    

        # Check for score milestones to add more aliens
        milestone = (score_value // 50) * 50
        if milestone > last_milestone and milestone >= 50:
            add_aliens(2)  # Add 2 more aliens every 50 points
            last_milestone = milestone
            print(f"Score reached {milestone}! Added 2 more aliens. Total aliens: {num_of_enemies}")

        # alien movement and collision detection
        for i in range(num_of_enemies): 
            # Check for game over condition
            if alienY[i] > 440:
                game_over = True
                # Move all aliens off screen
                for j in range(num_of_enemies):
                    alienY[j] = 2000  # Fixed: use j instead of i
                break  # Exit the alien loop
            
            alienX[i] += alienX_change[i]
            if alienX[i] <= 0:
                alienX_change[i] = 1
                alienY[i] += alienY_change[i]
            elif alienX[i] >= 736:
                alienX_change[i] = -1
                alienY[i] += alienY_change[i]

            # Check collision with all bullets
            for bullet in bullets[:]:  # Use slice copy for safe iteration
                if bullet['active']:
                    collision = isCollision(alienX[i], alienY[i], bullet['x'], bullet['y'])
                    if collision:
                        bullet['active'] = False  # Mark bullet as inactive
                        collision_sound.play()  # Play collision sound when alien is hit
                        score_value += 1
                        alienX[i] = randint(0,735)
                        alienY[i] = randint(50,100)
                        break  # Exit bullet loop after hit
            
            alien(alienX[i],alienY[i],i)

        # Update and draw bullets
        update_bullets()
        draw_bullets()   

    # Show game over text if game is over
    if game_over:
        game_over_text()

    player(playerX,playerY)
    show_score(textX,textY)
    
    pygame.display.update()