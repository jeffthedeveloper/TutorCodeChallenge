# Dungeon Explorer - Python Tutor Assessment Game
# Using only: PgZero, math, random, and Rect from Pygame
import pgzrun
import math
import random
import os
from pygame import Rect, K_RETURN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE

# declaring the variables / was necessary make the conversion for .ogg or .wav files
# to work with pgzrun / so i put the background original music in the music folder

music = sounds.background
hit_sound = sounds.hit
pickup_sound = sounds.pickup


# Function to safely handle missing sound and music files during development
def safe_play_sound(sound_name):
    if hasattr(sounds, sound_name):
        try:
            sounds.__getattr__(sound_name).play()
        except:
            pass

def safe_play_music(music_name):
    if hasattr(music, music_name):
        try:
            music.play(music_name)
        except:
            pass

# Constants
TITLE = "Dungeon Explorer"
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 32
PLAYER_SPEED = 3
ENEMY_SPEED = 1.5

# Game state
game_state = "menu"  # menu, playing, game_over
score = 0
high_score = 0
audio_enabled = True
level = 1

# Game grid
grid = []
grid_width = WIDTH // GRID_SIZE
grid_height = HEIGHT // GRID_SIZE

# Animation timers
animation_timer = 0
animation_speed = 10  # frames between animation updates

# Class definitions
class Character:
    def __init__(self, x, y, idle_images, walk_images):
        self.x = x
        self.y = y
        self.idle_images = idle_images
        self.walk_images = walk_images
        self.current_images = idle_images
        self.image_index = 0
        self.direction = 1  # 1 for right, -1 for left
        self.moving = False
        self.alive = True
        self.width = GRID_SIZE
        self.height = GRID_SIZE
    
    def update_animation(self):
        global animation_timer
        if animation_timer % animation_speed == 0:
            self.image_index = (self.image_index + 1) % len(self.current_images)
    
    def get_current_image(self):
        return self.current_images[self.image_index]
    
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def is_colliding(self, other):
        return self.get_rect().colliderect(other.get_rect())
    
    def draw(self):
        screen.blit(self.get_current_image(), (self.x, self.y))

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 
                         [images.hero_idle1, images.hero_idle2], 
                         [images.hero_walk1, images.hero_walk2])
        self.treasures = 0
        self.invulnerable_timer = 0
    
    def update(self):
        previous_x, previous_y = self.x, self.y
        self.moving = False
        
        if keyboard.left and self.x > 0:
            self.x -= PLAYER_SPEED
            self.direction = -1
            self.moving = True
        if keyboard.right and self.x < WIDTH - self.width:
            self.x += PLAYER_SPEED
            self.direction = 1
            self.moving = True
        if keyboard.up and self.y > 0:
            self.y -= PLAYER_SPEED
            self.moving = True
        if keyboard.down and self.y < HEIGHT - self.height:
            self.y += PLAYER_SPEED
            self.moving = True
        
        # Check for wall collisions
        for wall in walls:
            if self.get_rect().colliderect(wall.get_rect()):
                self.x, self.y = previous_x, previous_y
                break
        
        # Check for treasure collisions
        for treasure in treasures[:]:
            if self.get_rect().colliderect(treasure.get_rect()):
                treasures.remove(treasure)
                self.treasures += 1
                global score
                score += 100
                if audio_enabled and hasattr(sounds, 'pickup'):
                    sounds.pickup.play()
        
        # Update animation state
        if self.moving:
            self.current_images = self.walk_images
        else:
            self.current_images = self.idle_images
        
        self.update_animation()
        
        # Handle invulnerability timer
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 
                        [images.enemy_idle1, images.enemy_idle2], 
                        [images.enemy_walk1, images.enemy_walk2])
        self.move_timer = 0
        self.move_duration = random.randint(30, 90)
        self.move_direction = random.choice(['left', 'right', 'up', 'down'])
    
    def update(self):
        previous_x, previous_y = self.x, self.y
        
        # Handle movement based on current direction
        self.move_timer += 1
        if self.move_timer >= self.move_duration:
            self.move_timer = 0
            self.move_duration = random.randint(30, 90)
            self.move_direction = random.choice(['left', 'right', 'up', 'down'])
        
        if self.move_direction == 'left':
            self.x -= ENEMY_SPEED
            self.direction = -1
        elif self.move_direction == 'right':
            self.x += ENEMY_SPEED
            self.direction = 1
        elif self.move_direction == 'up':
            self.y -= ENEMY_SPEED
        elif self.move_direction == 'down':
            self.y += ENEMY_SPEED
        
        # Keep within screen bounds
        if self.x < 0:
            self.x = 0
            self.move_direction = 'right'
        elif self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            self.move_direction = 'left'
        if self.y < 0:
            self.y = 0
            self.move_direction = 'down'
        elif self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.move_direction = 'up'
        
        # Check for wall collisions
        for wall in walls:
            if self.get_rect().colliderect(wall.get_rect()):
                self.x, self.y = previous_x, previous_y
                # Change direction upon hitting a wall
                possible_directions = ['left', 'right', 'up', 'down']
                possible_directions.remove(self.move_direction)
                self.move_direction = random.choice(possible_directions)
                break
        
        # Update animation state
        self.moving = True
        if self.moving:
            self.current_images = self.walk_images
        else:
            self.current_images = self.idle_images
        
        self.update_animation()

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = GRID_SIZE
        self.height = GRID_SIZE
    
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        screen.blit(images.wall, (self.x, self.y))

class Treasure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = GRID_SIZE
        self.height = GRID_SIZE
    
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        screen.blit(images.treasure, (self.x, self.y))

# Game objects
player = Player(WIDTH // 2, HEIGHT // 2)
enemies = []
walls = []
treasures = []

# Button class for menu
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.hovered = False
    
    def draw(self):
        color = (100, 100, 200) if self.hovered else (70, 70, 170)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.rect(self.rect, (200, 200, 255))
        screen.draw.text(self.text, center=self.rect.center, fontsize=20, color=(255, 255, 255))
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

# Create menu buttons
start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, "Start Game")
audio_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "Sound: ON")
exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50, "Exit")

# Level generation
def generate_level(level_num):
    global player, enemies, walls, treasures
    
    # Clear existing objects
    enemies.clear()
    walls.clear()
    treasures.clear()
    
    # Set player position
    player.x = GRID_SIZE * 1
    player.y = GRID_SIZE * 1
    player.alive = True
    player.invulnerable_timer = 60  # Give player brief invulnerability
    
    # Create walls
    # Border walls
    for x in range(0, WIDTH, GRID_SIZE):
        walls.append(Wall(x, 0))
        walls.append(Wall(x, HEIGHT - GRID_SIZE))
    for y in range(0, HEIGHT, GRID_SIZE):
        walls.append(Wall(0, y))
        walls.append(Wall(WIDTH - GRID_SIZE, y))
    
    # Random walls
    num_internal_walls = 20 + level_num * 5
    for _ in range(num_internal_walls):
        x = random.randint(2, grid_width - 3) * GRID_SIZE
        y = random.randint(2, grid_height - 3) * GRID_SIZE
        
        # Ensure walls don't block player
        if not (x < GRID_SIZE * 3 and y < GRID_SIZE * 3):
            walls.append(Wall(x, y))
    
    # Add enemies
    num_enemies = 3 + level_num
    for _ in range(num_enemies):
        valid_position = False
        while not valid_position:
            x = random.randint(2, grid_width - 3) * GRID_SIZE
            y = random.randint(2, grid_height - 3) * GRID_SIZE
            
            # Check if position is valid
            test_enemy = Enemy(x, y)
            valid_position = True
            
            # Not too close to player
            if math.sqrt((player.x - x)**2 + (player.y - y)**2) < GRID_SIZE * 5:
                valid_position = False
                continue
            
            # Not colliding with walls
            for wall in walls:
                if test_enemy.get_rect().colliderect(wall.get_rect()):
                    valid_position = False
                    break
            
            # Not colliding with other enemies
            for enemy in enemies:
                if test_enemy.get_rect().colliderect(enemy.get_rect()):
                    valid_position = False
                    break
        
        enemies.append(Enemy(x, y))
    
    # Add treasures
    num_treasures = 5 + level_num
    for _ in range(num_treasures):
        valid_position = False
        while not valid_position:
            x = random.randint(2, grid_width - 3) * GRID_SIZE
            y = random.randint(2, grid_height - 3) * GRID_SIZE
            
            # Check if position is valid
            test_treasure = Treasure(x, y)
            valid_position = True
            
            # Not colliding with walls
            for wall in walls:
                if test_treasure.get_rect().colliderect(wall.get_rect()):
                    valid_position = False
                    break
            
            # Not colliding with other treasures
            for treasure in treasures:
                if test_treasure.get_rect().colliderect(treasure.get_rect()):
                    valid_position = False
                    break
            
            # Not colliding with enemies
            for enemy in enemies:
                if test_treasure.get_rect().colliderect(enemy.get_rect()):
                    valid_position = False
                    break
        
        treasures.append(Treasure(x, y))

# Update game state
def update():
    global animation_timer, game_state, high_score, score, level, audio_button, audio_enabled
    
    animation_timer += 1
    
    # Handle mouse for menu
    if game_state == "menu":
        # In PgZero, mouse is accessible through the 'mousepos' tuple instead
        try:
            # Try using the mouse position directly
            if 'mouse' in globals() and hasattr(mouse, 'x') and hasattr(mouse, 'y'):
                pos = (mouse.x, mouse.y)
            else:
                # If not available, default to center
                pos = (WIDTH // 2, HEIGHT // 2)
            
            start_button.check_hover(pos)
            audio_button.check_hover(pos)
            exit_button.check_hover(pos)
        except Exception as e:
            print(f"Error handling mouse: {e}")
        
        # Update audio button text
        audio_button.text = "Sound: ON" if audio_enabled else "Sound: OFF"
    
    # Update game objects if playing
    elif game_state == "playing":
        # Update player
        player.update()
        
        # Update enemies
        for enemy in enemies:
            enemy.update()
            
            # Check for collision with player
            if enemy.is_colliding(player) and player.invulnerable_timer <= 0:
                # Player is hit
                if audio_enabled and hasattr(sounds, 'hit'):
                    sounds.hit.play()
                game_state = "game_over"
                
                # Update high score
                if score > high_score:
                    high_score = score
        
        # Check if all treasures collected
        if not treasures:
            level += 1
            generate_level(level)

# Draw game elements
def draw():
    screen.clear()
    
    if game_state == "menu":
        # Draw menu background
        screen.fill((20, 20, 40))
        
        # Draw game title
        screen.draw.text("DUNGEON EXPLORER", centerx=WIDTH//2, centery=HEIGHT//4, 
                         fontsize=50, color=(255, 255, 255))
        
        # Draw instructions
        screen.draw.text("Arrow Keys to move, Collect treasures, Avoid enemies", 
                         centerx=WIDTH//2, centery=HEIGHT//3, fontsize=20, color=(200, 200, 200))
        
        # Draw buttons
        start_button.draw()
        audio_button.draw()
        exit_button.draw()
        
        # Draw high score
        if high_score > 0:
            screen.draw.text(f"High Score: {high_score}", centerx=WIDTH//2, centery=HEIGHT*4//5, 
                           fontsize=20, color=(255, 255, 100))
    
    elif game_state == "playing" or game_state == "game_over":
        # Draw floor tiles
        for y in range(0, HEIGHT, GRID_SIZE):
            for x in range(0, WIDTH, GRID_SIZE):
                screen.blit(images.floor, (x, y))
        
        # Draw walls
        for wall in walls:
            wall.draw()
        
        # Draw treasures
        for treasure in treasures:
            treasure.draw()
        
        # Draw enemies
        for enemy in enemies:
            enemy.draw()
        
        # Draw player (flicker if invulnerable)
        if player.invulnerable_timer <= 0 or animation_timer % 4 < 2:
            player.draw()
        
        # Draw score
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=20, color=(255, 255, 255))
        screen.draw.text(f"Level: {level}", (10, 40), fontsize=20, color=(255, 255, 255))
        
        
        
        # Draw game over screen
        if game_state == "game_over":
            screen.draw.filled_rect(Rect(WIDTH//4, HEIGHT//3, WIDTH//2, HEIGHT//3), (0, 0, 0, 180))
            screen.draw.text("GAME OVER", centerx=WIDTH//2, centery=HEIGHT//2 - 40, 
                           fontsize=40, color=(255, 50, 50))
            screen.draw.text(f"Final Score: {score}", centerx=WIDTH//2, centery=HEIGHT//2, 
                           fontsize=30, color=(255, 255, 255))
            screen.draw.text("Press ENTER to play again", centerx=WIDTH//2, centery=HEIGHT//2 + 40, 
                           fontsize=20, color=(200, 200, 200))

# Mouse handlers
def on_mouse_down(pos, button):
    if game_state == "menu":
        if start_button.check_click(pos):
            start_game()
        elif audio_button.check_click(pos):
            global audio_enabled
            audio_enabled = not audio_enabled
        elif exit_button.check_click(pos):
            exit()

# Keyboard handlers
def on_key_down(key):
    global game_state, score
    
    if game_state == "menu" and key == keys.RETURN:
        start_game()
    elif game_state == "game_over" and key == keys.RETURN:
        score = 0
        game_state = "playing"
        generate_level(1)

def start_game():
    global game_state, score, level
    game_state = "playing"
    score = 0
    level = 1
    generate_level(level)
    if audio_enabled and hasattr(music, 'background'):
        music.play('background')
        music.play(-1)  # Loop the background music

# Initialize the game
generate_level(level)

# Start the game
pgzrun.go()