# Dungeon Explorer - Python Tutor Assessment Game
# Using only: PgZero, math, random, and Rect from Pygame
import pgzrun
import math
import random
import os
from pygame import Rect, K_RETURN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE
import pygame  # Importar pygame apenas para carregar sons toda a logica foi feita com pgzero

# Configuração inicial do mouse
pygame.mouse.set_visible(True)

# verificando inicialização do pygame mixer
if not pygame.mixer.get_init():
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
print(f"Disponíveis em sounds: {dir(sounds)}")  # Verifique quais sons estão carregados

# Inicialização dos sons
pygame.mixer.init()
try:
    sounds.background = pygame.mixer.Sound('music/background.ogg')
    sounds.hit = pygame.mixer.Sound('sounds/hit.ogg')
    sounds.pickup = pygame.mixer.Sound('sounds/pickup.ogg')
    print("Sons carregados com sucesso!")  # Debug
except Exception as e:
    print(f"Erro ao carregar sons: {e}")
    # Cria sons vazios para evitar erros
    sounds.background = None
    sounds.hit = None
    sounds.pickup = None

# Estados do jogo
jogo_comecou = False
music_playing = False
menu_aberto = True  # O menu começa aberto
audio_feedback_timer = 0  # Timer para feedback visual do áudio

# Function to safely handle missing sound and music files during development
def safe_play_sound(sound_name):
    if not audio_enabled:
        return
        
    sound = getattr(sounds, sound_name, None)
    if sound is not None:
        try:
            sound.play()
        except Exception as e:
            print(f"Erro ao tocar som {sound_name}: {e}")

def safe_play_music(force_stop=False):
    global music_playing
    if force_stop:
        if music_playing and sounds.background:
            sounds.background.stop()
            music_playing = False
        return
    
    if audio_enabled and sounds.background and not music_playing and not jogo_comecou:
        try:
            sounds.background.play(-1)  # Toca em loop
            music_playing = True
        except Exception as e:
            print(f"Erro ao tocar música de fundo: {e}")
    elif not audio_enabled and music_playing:
        try:
            sounds.background.stop()
            music_playing = False
        except Exception as e:
            print(f"Erro ao parar música de fundo: {e}")
    elif jogo_comecou and music_playing:
        try:
            sounds.background.stop()
            music_playing = False
        except Exception as e:
            print(f"Erro ao parar música de fundo: {e}")

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
class CollisionHandler:
    @staticmethod
    def precise_collision(rect, walls):
        """Verificação de colisão com margem de segurança"""
        margin = 2  # Margem de pixels para evitar colisões fantasmas
        test_rect = rect.inflate(-margin, -margin)  # Reduz o retângulo
        
        for wall in walls:
            if test_rect.colliderect(wall.get_rect()):
                return True
        return False

    @staticmethod
    def can_move(character, walls, dx, dy):
        """Verifica movimento com tratamento de cantos"""
        test_rect = Rect(character.x + dx, character.y + dy, 
                        character.width, character.height)
        
        # Verifica colisão com margem
        if not CollisionHandler.precise_collision(test_rect, walls):
            return True
            
        # Tenta movimento parcial (deslize em paredes)
        if dx != 0 and not CollisionHandler.precise_collision(
            Rect(character.x + dx, character.y, character.width, character.height), walls):
            return True
            
        if dy != 0 and not CollisionHandler.precise_collision(
            Rect(character.x, character.y + dy, character.width, character.height), walls):
            return True
            
        return False

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
        # Guarda posição anterior
        previous_x, previous_y = self.x, self.y
        
        # Controle de movimento
        dx, dy = 0, 0
        if keyboard.left: dx = -PLAYER_SPEED
        if keyboard.right: dx = PLAYER_SPEED
        if keyboard.up: dy = -PLAYER_SPEED
        if keyboard.down: dy = PLAYER_SPEED

        # Normalização diagonal
        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        # Verificação de colisão com paredes
        if CollisionHandler.can_move(self, walls, dx, dy):
            self.x += dx
            self.y += dy
            self.moving = dx != 0 or dy != 0
        else:
            self.x, self.y = previous_x, previous_y
            self.moving = False

        # Verificação de tesouros
        for treasure in treasures[:]:
            if self.get_rect().colliderect(treasure.get_rect()):
                treasures.remove(treasure)
                self.treasures += 1
                global score
                score += 100
                if audio_enabled:
                    safe_play_sound('pickup')

        # Verificação de inimigos
        for enemy in enemies:
            if self.get_rect().colliderect(enemy.get_rect()) and self.invulnerable_timer <= 0:
                if audio_enabled:
                    safe_play_sound('hit')
                global game_state
                game_state = "game_over"
                if score > high_score:
                    high_score = score

        # Atualização de animação
        if self.moving:
            self.current_images = self.walk_images
        else:
            self.current_images = self.idle_images
        self.update_animation()

        # Temporizador de invulnerabilidade
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
                if self.move_direction in possible_directions:
                    possible_directions.remove(self.move_direction)
                if possible_directions:
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

# Button class for menu and in-game
class Button:
    def __init__(self, x, y, width, height, text, in_game=False):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        self.in_game = in_game  # Se é um botão in-game

    def draw(self):
        if self.in_game:
            # Estilo minimalista para botões in-game
            color = (0, 0, 0, 150) if self.hovered else (0, 0, 0, 100)
            screen.draw.filled_rect(self.rect, color)
            screen.draw.text(self.text, center=self.rect.center, fontsize=16, color=(255, 255, 255))
        else:
            # Estilo normal para menu
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

# Create in-game audio button
in_game_audio_button = Button(WIDTH - 120, 10, 110, 30, "Sound: ON", True)

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
    global animation_timer, game_state, high_score, score, level, audio_button, audio_enabled, music_playing, jogo_comecou, audio_feedback_timer

    safe_play_music()
    animation_timer += 1
    
    # Decrementa o timer de feedback do áudio
    if audio_feedback_timer > 0:
        audio_feedback_timer -= 1

    # Handle mouse for menu - versão mais segura
    if game_state == "menu":
        try:
            if hasattr(mouse, 'pos') and mouse.pos is not None:
                start_button.check_hover(mouse.pos)
                audio_button.check_hover(mouse.pos)
                exit_button.check_hover(mouse.pos)
        except Exception as e:
            print(f"Erro no mouse handling: {str(e)}")

    # Handle mouse for in-game audio button
    elif game_state == "playing":
        try:
            if hasattr(mouse, 'pos') and mouse.pos is not None:
                in_game_audio_button.check_hover(mouse.pos)
        except Exception as e:
            print(f"Erro no mouse handling in-game: {str(e)}")

        # Update player
        player.update()

        # Update enemies
        for enemy in enemies:
            enemy.update()

            # Check for collision with player
            if enemy.is_colliding(player) and player.invulnerable_timer <= 0:
                # Player is hit
                if audio_enabled:
                    safe_play_sound('hit')
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
        # Atualização do menu (hover dos botões)
        mouse_pos = pygame.mouse.get_pos() if pygame.mouse.get_focused() else None
        if mouse_pos:
            start_button.check_hover(mouse_pos)
            audio_button.check_hover(mouse_pos)
            exit_button.check_hover(mouse_pos)
            
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
            screen.draw.text(f"High Score: {high_score}", centerx=WIDTH//2, centery=HEIGHT*4//5, fontsize=20, color=(255, 255, 100))

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

        # Draw in-game audio button
        if game_state == "playing":
            in_game_audio_button.text = "Sound: ON" if audio_enabled else "Sound: OFF"
            in_game_audio_button.draw()
            
            # Draw feedback visual
            if audio_feedback_timer > 0:
                screen.draw.text("✓", (in_game_audio_button.rect.right + 5, in_game_audio_button.rect.y + 5), 
                                fontsize=20, color=(0, 255, 0))

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
    global game_state, audio_enabled, audio_feedback_timer
    
    if game_state == "menu":
        if start_button.check_click(pos):
            start_game()
        elif audio_button.check_click(pos):
            audio_enabled = not audio_enabled
            audio_button.text = "Sound: ON" if audio_enabled else "Sound: OFF"
            if audio_enabled:
                safe_play_music()
            else:
                safe_play_music(force_stop=True)
        elif exit_button.check_click(pos):
            exit()
    
    elif game_state == "playing":
        # Verifica clique no botão de áudio durante o jogo
        if in_game_audio_button.check_click(pos):
            audio_enabled = not audio_enabled
            audio_feedback_timer = 30  # 0.5 segundos de feedback (considerando 60 FPS)
            # Atualiza imediatamente o estado do áudio
            if audio_enabled:
                safe_play_music()
            else:
                safe_play_music(force_stop=True)

# Keyboard handlers
def on_key_down(key):
    global game_state, score, level, jogo_comecou, menu_aberto

    if game_state == "menu" and key == keys.RETURN:
        start_game()
        menu_aberto = False

    elif game_state == "game_over" and key == keys.RETURN:
        score = 0
        level = 1
        game_state = "playing"
        generate_level(level)
        menu_aberto = False
        
def start_game():
    global game_state, score, level, jogo_comecou, music_playing
    game_state = "playing"
    score = 0
    level = 1
    jogo_comecou = True
    generate_level(level)
    # Para a música do menu se estiver tocando
    if music_playing:
        safe_play_music(force_stop=True)
    
    # Se o áudio estiver habilitado, toca a música do jogo
    if audio_enabled and sounds.background:
        try:
            sounds.background.play(-1)
            music_playing = True
        except Exception as e:
            print(f"Erro ao tocar música ao iniciar o jogo: {e}")
            
# Initialize the game
generate_level(level)
safe_play_music() # Tentar tocar a música no início

# Start the game
pgzrun.go()