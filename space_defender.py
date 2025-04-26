# Space Defender - Python Tutor Assessment Game
# Using only: PgZero, math, random, and Rect from Pygame
import pgzrun
import math
import random
from pygame import Rect

# Constants
TITLE = "Space Defender"
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2
ASTEROID_SPEED_MIN = 1
ASTEROID_SPEED_MAX = 4
MAX_ASTEROIDS = 8
MAX_ENEMIES = 5
SPAWN_DELAY = 180  # frames

# Game state
game_over = False
score = 0
high_score = 0
spawn_timer = 0
game_started = False

# Initialize player
player = Actor('ship')
player.pos = (WIDTH // 2, HEIGHT - 50)
player.alive = True

# Initialize game objects
bullets = []
enemies = []
asteroids = []
explosions = []

# Background stars (simulated with Rect objects)
stars = []
for _ in range(100):
    star_size = random.randint(1, 3)
    stars.append({
        'rect': Rect((random.randint(0, WIDTH), random.randint(0, HEIGHT)), (star_size, star_size)),
        'speed': random.uniform(0.2, 1.0)
    })

# Function to reset the game
def reset_game():
    global game_over, score, player, bullets, enemies, asteroids, explosions, spawn_timer
    
    game_over = False
    score = 0
    spawn_timer = 0
    
    player.pos = (WIDTH // 2, HEIGHT - 50)
    player.alive = True
    
    bullets.clear()
    enemies.clear()
    asteroids.clear()
    explosions.clear()

# Update game state
def update():
    global spawn_timer, game_over, score, high_score, game_started
    
    # Don't update if game hasn't started
    if not game_started:
        return
    
    # Don't update if game is over
    if game_over:
        return
    
    # Update player movement
    update_player()
    
    # Update bullets
    update_bullets()
    
    # Update enemies
    update_enemies()
    
    # Update asteroids
    update_asteroids()
    
    # Update explosions
    update_explosions()
    
    # Update spawn timer
    spawn_timer += 1
    if spawn_timer >= SPAWN_DELAY:
        spawn_timer = 0
        if len(asteroids) < MAX_ASTEROIDS:
            spawn_asteroid()
        if len(enemies) < MAX_ENEMIES:
            spawn_enemy()
    
    # Move stars (parallax background effect)
    for star in stars:
        star['rect'].y += star['speed']
        if star['rect'].top > HEIGHT:
            star['rect'].top = 0
            star['rect'].x = random.randint(0, WIDTH)
    
    # Update high score
    if score > high_score:
        high_score = score

def update_player():
    # Movement controls
    if keyboard.left and player.left > 0:
        player.x -= PLAYER_SPEED
    if keyboard.right and player.right < WIDTH:
        player.x += PLAYER_SPEED
    if keyboard.up and player.top > 0:
        player.y -= PLAYER_SPEED
    if keyboard.down and player.bottom < HEIGHT:
        player.y += PLAYER_SPEED
    
    # Shooting
    if keyboard.space:
        try_to_fire()

# Firing mechanism with cooldown
last_shot = 0
def try_to_fire():
    global last_shot
    current_time = pygame.time.get_ticks()
    # Only allow firing every 250 milliseconds
    if current_time - last_shot > 250:
        # Create a new bullet
        bullet = {
            'rect': Rect((player.center[0] - 2, player.top), (4, 10)),
            'speed': BULLET_SPEED
        }
        bullets.append(bullet)
        sounds.laser.play()
        last_shot = current_time

def update_bullets():
    # Move bullets and check for collisions
    for bullet in bullets[:]:
        # Move bullet up
        bullet['rect'].y -= bullet['speed']
        
        # Remove if off screen
        if bullet['rect'].bottom < 0:
            bullets.remove(bullet)
            continue
        
        # Check collision with enemies
        for enemy in enemies[:]:
            if bullet['rect'].colliderect(enemy['rect']):
                enemies.remove(enemy)
                bullets.remove(bullet)
                add_explosion(enemy['rect'].center)
                sounds.explosion.play()
                global score
                score += 100
                break

def update_enemies():
    # Move enemies and check for collisions
    for enemy in enemies[:]:
        # Move enemy down
        enemy['rect'].y += enemy['speed']
        
        # Remove if off screen
        if enemy['rect'].top > HEIGHT:
            enemies.remove(enemy)
            continue
        
        # Check collision with player
        if player.alive and enemy['rect'].colliderect(player.colliderrect()):
            player_hit()
            enemies.remove(enemy)
            add_explosion(enemy['rect'].center)
            sounds.explosion.play()

def update_asteroids():
    # Move asteroids and check for collisions
    for asteroid in asteroids[:]:
        # Move asteroid down
        asteroid['rect'].x += asteroid['x_speed']
        asteroid['rect'].y += asteroid['y_speed']
        
        # Bounce off walls
        if asteroid['rect'].left < 0 or asteroid['rect'].right > WIDTH:
            asteroid['x_speed'] *= -1
        
        # Remove if off bottom of screen
        if asteroid['rect'].top > HEIGHT:
            asteroids.remove(asteroid)
            continue
        
        # Check collision with player
        if player.alive and asteroid['rect'].colliderect(player.colliderrect()):
            player_hit()
            asteroids.remove(asteroid)
            add_explosion(asteroid['rect'].center)
            sounds.explosion.play()
        
        # Check collision with bullets
        for bullet in bullets[:]:
            if asteroid['rect'].colliderect(bullet['rect']):
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                add_explosion(asteroid['rect'].center)
                sounds.explosion.play()
                global score
                score += 50
                break

def update_explosions():
    # Update explosion animations
    for explosion in explosions[:]:
        explosion['timer'] -= 1
        if explosion['timer'] <= 0:
            explosions.remove(explosion)

def spawn_asteroid():
    size = random.randint(20, 40)
    x_pos = random.randint(size, WIDTH - size)
    
    asteroid = {
        'rect': Rect((x_pos, -size), (size, size)),
        'x_speed': random.uniform(-2, 2),
        'y_speed': random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
    }
    
    asteroids.append(asteroid)

def spawn_enemy():
    enemy_width, enemy_height = 40, 40
    x_pos = random.randint(enemy_width, WIDTH - enemy_width)
    
    enemy = {
        'rect': Rect((x_pos, -enemy_height), (enemy_width, enemy_height)),
        'speed': ENEMY_SPEED
    }
    
    enemies.append(enemy)

def add_explosion(position):
    explosion = {
        'pos': position,
        'timer': 20,
        'radius': 0,
        'max_radius': 30
    }
    explosions.append(explosion)

def player_hit():
    global game_over
    player.alive = False
    game_over = True
    add_explosion(player.center)
    sounds.explosion.play()

# Draw game elements
def draw():
    screen.clear()
    
    # Draw starfield background
    screen.fill((0, 0, 20))
    
    # Draw stars
    for star in stars:
        screen.draw.filled_rect(star['rect'], (200, 200, 255))
    
    # Draw game or start screen
    if not game_started:
        draw_start_screen()
    else:
        # Draw game elements
        if player.alive:
            player.draw()
        
        # Draw bullets
        for bullet in bullets:
            screen.draw.filled_rect(bullet['rect'], (255, 0, 0))
        
        # Draw enemies
        for enemy in enemies:
            screen.draw.filled_rect(enemy['rect'], (0, 255, 0))
        
        # Draw asteroids
        for asteroid in asteroids:
            screen.draw.filled_circle(
                (asteroid['rect'].centerx, asteroid['rect'].centery),
                asteroid['rect'].width // 2,
                (150, 150, 150)
            )
        
        # Draw explosions
        for explosion in explosions:
            radius = min(explosion['max_radius'], 
                          explosion['radius'] + (explosion['max_radius'] * (20 - explosion['timer']) // 20))
            screen.draw.circle(
                explosion['pos'],
                radius,
                (255, 200, 50)
            )
        
        # Draw score
        screen.draw.text(f"Score: {score}", (10, 10), color=(255, 255, 255))
        screen.draw.text(f"High Score: {high_score}", (WIDTH - 150, 10), color=(255, 255, 255))
        
        # Draw game over screen
        if game_over:
            draw_game_over()

def draw_start_screen():
    # Draw title
    screen.draw.text("SPACE DEFENDER", centerx=WIDTH//2, centery=HEIGHT//3, 
                     fontsize=60, color=(255, 255, 255))
    
    # Draw instructions
    screen.draw.text("Arrow Keys to move, Space to shoot", 
                     centerx=WIDTH//2, centery=HEIGHT//2, fontsize=30, color=(200, 200, 200))
    
    # Draw start prompt
    screen.draw.text("Press ENTER to start", 
                     centerx=WIDTH//2, centery=HEIGHT*2//3, fontsize=40, color=(255, 255, 100))

def draw_game_over():
    screen.draw.text("GAME OVER", centerx=WIDTH//2, centery=HEIGHT//3, 
                     fontsize=60, color=(255, 50, 50))
    screen.draw.text(f"Final Score: {score}", centerx=WIDTH//2, centery=HEIGHT//2, 
                     fontsize=40, color=(255, 255, 255))
    screen.draw.text("Press ENTER to play again", centerx=WIDTH//2, centery=HEIGHT*2//3, 
                     fontsize=30, color=(200, 200, 200))

# Handle keyboard input
def on_key_down(key):
    global game_started
    
    if key == keys.RETURN:
        if not game_started:
            game_started = True
        elif game_over:
            reset_game()

# Main entry point
pgzrun.go()
