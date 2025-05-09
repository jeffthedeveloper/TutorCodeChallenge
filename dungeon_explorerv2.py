# Dungeon Explorer - Python Tutor Assessment Game
# Using only: PgZero, math, random, and Rect from Pygame
import pgzrun
import math
import random
from pygame import Rect

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
    
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
    
    def update_animation(self):
        # Update animation frame
        if animation_timer % animation_speed == 0:
            self.image_index = (self.image_index + 1) % len(self.current_images)
    
    def draw(self):
        # Get current image based on direction and animation frame
        image = self.current_images[self.image_index]
        
        # Draw with correct orientation
        if self.direction < 0:
            # Flip the image for left-facing direction
            screen.blit(image, (self.x, self.y), flipx=True)
        else:
            screen.blit(image, (self.x, self.y))
    
    def is_colliding(self, other):
        return self.get_rect().colliderect(other.get_rect())
       
class Player(Character):
    def __init__(self, x, y):
        idle_images = [images.hero_idle1, images.hero_idle2]
        walk_images = [images.hero_walk1, images.hero_walk2]
        super().__init__(x, y, idle_images, walk_images)
        self.treasures = 0
        self.invulnerable_timer = 0
        self.last_direction = 1  # Para animações mais consistentes
    
    def update(self):
        # Sistema de movimento avançado com separação de eixos
        previous_x, previous_y = self.x, self.y
        self.moving = False
        dx, dy = 0, 0
        
        # Controles horizontais (eixo X)
        if keyboard.left and self.x > 0:
            dx = -PLAYER_SPEED
            self.direction = -1
            self.last_direction = -1
            self.moving = True
            
        if keyboard.right and self.x < WIDTH - self.width:
            dx = PLAYER_SPEED
            self.direction = 1
            self.last_direction = 1
            self.moving = True
        
        # Aplicar movimento X com tratamento de colisão
        if dx != 0:
            self.x += dx
            # Verificação de colisão otimizada
            player_rect = self.get_rect()
            if any(player_rect.colliderect(wall.get_rect()) for wall in walls):
                self.x = previous_x
                dx = 0  # Movimento bloqueado no eixo X
        
        # Controles verticais (eixo Y)
        if keyboard.up and self.y > 0:
            dy = -PLAYER_SPEED
            self.moving = True
            
        if keyboard.down and self.y < HEIGHT - self.height:
            dy = PLAYER_SPEED
            self.moving = True
        
        # Aplicar movimento Y com tratamento de colisão
        if dy != 0:
            self.y += dy
            player_rect = self.get_rect()
            if any(player_rect.colliderect(wall.get_rect()) for wall in walls):
                self.y = previous_y
                dy = 0  # Movimento bloqueado no eixo Y
        
        # Sistema de coleta de tesouros
        for treasure in treasures[:]:
            if self.get_rect().colliderect(treasure.get_rect()):
                treasures.remove(treasure)
                self.treasures += 1
                global score
                score += 100
                if audio_enabled and hasattr(sounds, 'pickup'):
                    sounds.pickup.play()
        
        # Sistema de animação aprimorado
        self.handle_animation(dx, dy)
        
        # Temporizador de invulnerabilidade
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
    
    def handle_animation(self, dx, dy):
        """Sistema completo de gerenciamento de animações"""
        # Transição suave entre estados de movimento
        if dx != 0 or dy != 0:
            self.current_images = self.walk_images
            # Ajuste fino: mantém a direção mesmo quando parado momentaneamente
            self.direction = self.last_direction
        else:
            self.current_images = self.idle_images
        
        # Atualização do frame de animação
        self.update_animation()
            
class Enemy(Character):
    def __init__(self, x, y):
        idle_images = [images.enemy_idle1, images.enemy_idle2]
        walk_images = [images.enemy_walk1, images.enemy_walk2]
        super().__init__(x, y, idle_images, walk_images)
        self.move_timer = 0
        self.move_duration = random.randint(30, 90)
        self.move_direction = random.choice(['left', 'right', 'up', 'down'])
            
    def update(self):
        previous_x, previous_y = self.x, self.y
        
        # Lidar com o movimento baseado na direção atual
        self.move_timer += 1
        if self.move_timer >= self.move_duration:
            self.move_timer = 0
            self.move_duration = random.randint(30, 90)
            self.move_direction = random.choice(['left', 'right', 'up', 'down'])
        
        # Mover em eixos separados
        dx, dy = 0, 0
        
        if self.move_direction == 'left':
            dx = -ENEMY_SPEED
            self.direction = -1
        elif self.move_direction == 'right':
            dx = ENEMY_SPEED
            self.direction = 1
        elif self.move_direction == 'up':
            dy = -ENEMY_SPEED
        elif self.move_direction == 'down':
            dy = ENEMY_SPEED
        
        # Aplicar movimento no eixo X e verificar colisões
        if dx != 0:
            self.x += dx
            # Manter dentro dos limites da tela
            if self.x < 0:
                self.x = 0
                self.move_direction = 'right'
            elif self.x > WIDTH - self.width:
                self.x = WIDTH - self.width
                self.move_direction = 'left'
            
            # Verificar colisões com paredes
            x_collision = False
            for wall in walls:
                if self.get_rect().colliderect(wall.get_rect()):
                    x_collision = True
                    break
            
            if x_collision:
                self.x = previous_x
                if self.move_direction == 'left':
                    self.move_direction = 'right'
                elif self.move_direction == 'right':
                    self.move_direction = 'left'
        
        # Aplicar movimento no eixo Y e verificar colisões
        if dy != 0:
            self.y += dy
            # Manter dentro dos limites da tela
            if self.y < 0:
                self.y = 0
                self.move_direction = 'down'
            elif self.y > HEIGHT - self.height:
                self.y = HEIGHT - self.height
                self.move_direction = 'up'
            
            # Verificar colisões com paredes
            y_collision = False
            for wall in walls:
                if self.get_rect().colliderect(wall.get_rect()):
                    y_collision = True
                    break
            
            if y_collision:
                self.y = previous_y
                if self.move_direction == 'up':
                    self.move_direction = 'down'
                elif self.move_direction == 'down':
                    self.move_direction = 'up'
        
        # Atualizar estado da animação
        self.moving = dx != 0 or dy != 0
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

def generate_level(level_num):
    global player, enemies, walls, treasures
    
    # Limpar objetos existentes
    enemies.clear()
    walls.clear()
    treasures.clear()
    
    # Configurar posição inicial do jogador
    player.x = GRID_SIZE * 1
    player.y = GRID_SIZE * 1
    player.alive = True
    player.invulnerable_timer = 60
    
    # Criar paredes
    # Paredes das bordas
    for x in range(0, WIDTH, GRID_SIZE):
        walls.append(Wall(x, 0))
        walls.append(Wall(x, HEIGHT - GRID_SIZE))
    for y in range(0, HEIGHT, GRID_SIZE):
        walls.append(Wall(0, y))
        walls.append(Wall(WIDTH - GRID_SIZE, y))
    
    # Paredes internas com espaçamento
    num_internal_walls = 20 + level_num * 5
    for i in range(num_internal_walls):
        valid_wall = False
        while not valid_wall:
            x = random.randint(2, grid_width - 3) * GRID_SIZE
            y = random.randint(2, grid_height - 3) * GRID_SIZE
            new_wall = Wall(x, y)
            
            # Verificar distância de outras paredes
            too_close = any(
                abs(x - wall.x) < GRID_SIZE*1.5 and abs(y - wall.y) < GRID_SIZE*1.5
                for wall in walls
            )
            
            # Garantir área inicial livre
            if not too_close and not (x < GRID_SIZE*3 and y < GRID_SIZE*3):
                walls.append(new_wall)
                valid_wall = True
    
    # Adicionar inimigos
    num_enemies = 3 + level_num
    for i in range(num_enemies):
        valid_position = False
        attempts = 0
        while not valid_position and attempts < 100:
            x = random.randint(2, grid_width - 3) * GRID_SIZE
            y = random.randint(2, grid_height - 3) * GRID_SIZE
            enemy_rect = Rect(x, y, GRID_SIZE, GRID_SIZE)
            valid_position = True
            
            # Distância do jogador
            if math.hypot(player.x - x, player.y - y) < GRID_SIZE * 5:
                valid_position = False
            
            # Colisão com paredes
            if valid_position:
                for wall in walls:
                    if enemy_rect.colliderect(wall.get_rect()):
                        valid_position = False
                        break
            
            # Colisão com outros inimigos
            if valid_position:
                for enemy in enemies:
                    if enemy_rect.colliderect(Rect(enemy.x, enemy.y, GRID_SIZE, GRID_SIZE)):
                        valid_position = False
                        break
            
            attempts += 1
        
        if valid_position:
            enemies.append(Enemy(x, y))
    
    # Adicionar tesouros (mesma lógica dos inimigos)
    num_treasures = 5 + level_num
    for i in range(num_treasures):
        valid_position = False
        attempts = 0
        while not valid_position and attempts < 100:
            x = random.randint(2, grid_width - 3) * GRID_SIZE
            y = random.randint(2, grid_height - 3) * GRID_SIZE
            treasure_rect = Rect(x, y, GRID_SIZE, GRID_SIZE)
            valid_position = True
            
            # Verificar colisões
            for wall in walls:
                if treasure_rect.colliderect(wall.get_rect()):
                    valid_position = False
                    break
            
            if valid_position:
                for enemy in enemies:
                    if treasure_rect.colliderect(Rect(enemy.x, enemy.y, GRID_SIZE, GRID_SIZE)):
                        valid_position = False
                        break
            
            if valid_position:
                for treasure in treasures:
                    if treasure_rect.colliderect(treasure.get_rect()):
                        valid_position = False
                        break
            
            attempts += 1
        
        if valid_position:
            treasures.append(Treasure(x, y))

# Update game state
def update():
    global animation_timer, game_state, high_score, score, level, audio_enabled
    
    animation_timer += 1
    
    # Handle mouse for menu
    if game_state == "menu":
        # In PgZero, use pos directly
        pos = (pygame.mouse.get_pos() if 'pygame' in globals() and hasattr(pygame, 'mouse') 
               else (WIDTH // 2, HEIGHT // 2))
        
        start_button.check_hover(pos)
        audio_button.check_hover(pos)
        exit_button.check_hover(pos)
        
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
    global game_state, score, level
    
    if game_state == "menu" and key == keys.RETURN:
        start_game()
    elif game_state == "game_over" and key == keys.RETURN:
        score = 0
        level = 1
        game_state = "playing"
        generate_level(level)

def start_game():
    global game_state, score, level
    game_state = "playing"
    score = 0
    level = 1
    generate_level(level)
    if audio_enabled and hasattr(music, 'background'):
        music.play('background')

# Initialize the game
generate_level(level)

# Start the game
pgzrun.go()