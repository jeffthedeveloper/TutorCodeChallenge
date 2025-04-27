import pgzrun
import math
import random
from pygame import Rect

# Configurações
WIDTH, HEIGHT = 800, 600
TITLE = "Dungeon Explorer Minimalista"
GRID_SIZE = 32
PLAYER_SPEED = 3
ENEMY_SPEED = 1.5

# Estados do jogo
game_state = "menu"  # menu, playing, game_over
score = 0
high_score = 0
audio_enabled = True
level = 1
animation_timer = 0

# Classes do jogo
class Character:
    def __init__(self, x, y, idle_images, walk_images):
        self.x, self.y = x, y
        self.idle_images = idle_images
        self.walk_images = walk_images
        self.current_images = idle_images
        self.image_index = 0
        self.direction = 1
        self.moving = False
        self.width = self.height = GRID_SIZE
        
    def update_animation(self):
        global animation_timer
        if animation_timer % 10 == 0:
            self.image_index = (self.image_index + 1) % len(self.current_images)
    
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        screen.blit(self.current_images[self.image_index], (self.x, self.y))

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 
                        [images.hero_idle1, images.hero_idle2],
                        [images.hero_walk1, images.hero_walk2])
        self.invulnerable_timer = 60
        
    def update(self):
        dx, dy = 0, 0
        if keyboard.left: dx = -PLAYER_SPEED
        if keyboard.right: dx = PLAYER_SPEED
        if keyboard.up: dy = -PLAYER_SPEED
        if keyboard.down: dy = PLAYER_SPEED
        
        # Normalizar movimento diagonal
        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071
            
        # Verificar colisões
        test_rect = Rect(self.x + dx, self.y + dy, self.width, self.height)
        if not any(test_rect.colliderect(wall.get_rect()) for wall in walls):
            self.x += dx
            self.y += dy
            self.moving = dx != 0 or dy != 0
            
        # Verificar coleta de tesouros
        for treasure in treasures[:]:
            if self.get_rect().colliderect(treasure.get_rect()):
                treasures.remove(treasure)
                global score
                score += 100
                if audio_enabled:
                    sounds.pickup.play()
                
        # Verificar colisões com inimigos
        if self.invulnerable_timer <= 0:
            for enemy in enemies:
                if self.get_rect().colliderect(enemy.get_rect()):
                    global game_state
                    game_state = "game_over"
                    if score > high_score:
                        global high_score
                        high_score = score
                    if audio_enabled:
                        sounds.hit.play()
        else:
            self.invulnerable_timer -= 1
            
        # Atualizar animação
        self.current_images = self.walk_images if self.moving else self.idle_images
        self.update_animation()

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 
                        [images.enemy_idle1, images.enemy_idle2],
                        [images.enemy_walk1, images.enemy_walk2])
        self.move_timer = 0
        self.move_duration = random.randint(30, 90)
        self.move_direction = random.choice(['left', 'right', 'up', 'down'])
        
    def update(self):
        prev_x, prev_y = self.x, self.y
        
        # Atualizar temporizador de movimento
        self.move_timer += 1
        if self.move_timer >= self.move_duration:
            self.move_timer = 0
            self.move_duration = random.randint(30, 90)
            self.move_direction = random.choice(['left', 'right', 'up', 'down'])
            
        # Movimentar inimigo
        if self.move_direction == 'left': self.x -= ENEMY_SPEED
        elif self.move_direction == 'right': self.x += ENEMY_SPEED
        elif self.move_direction == 'up': self.y -= ENEMY_SPEED
        elif self.move_direction == 'down': self.y += ENEMY_SPEED
        
        # Verificar colisões com paredes
        if (self.x < 0 or self.x > WIDTH - self.width or
            self.y < 0 or self.y > HEIGHT - self.height or
            any(self.get_rect().colliderect(wall.get_rect()) for wall in walls)):
            self.x, self.y = prev_x, prev_y
            self.move_direction = random.choice(['left', 'right', 'up', 'down'])
            
        # Atualizar animação
        self.current_images = self.walk_images
        self.update_animation()

class Wall:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width = self.height = GRID_SIZE
        
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        screen.blit(images.wall, (self.x, self.y))

class Treasure:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width = self.height = GRID_SIZE
        
    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        screen.blit(images.treasure, (self.x, self.y))

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

# Botões do menu
start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, "Começar Jogo")
audio_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "Som: ON")
exit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50, "Sair")

# Listas de objetos
player = None
enemies = []
walls = []
treasures = []

def generate_level(level_num):
    global player, enemies, walls, treasures
    
    # Limpar objetos existentes
    enemies.clear()
    walls.clear()
    treasures.clear()
    
    # Inicializar jogador
    player = Player(GRID_SIZE, GRID_SIZE)
    player.invulnerable_timer = 60
    
    # Criar paredes de borda
    for x in range(0, WIDTH, GRID_SIZE):
        walls.append(Wall(x, 0))
        walls.append(Wall(x, HEIGHT - GRID_SIZE))
    for y in range(0, HEIGHT, GRID_SIZE):
        walls.append(Wall(0, y))
        walls.append(Wall(WIDTH - GRID_SIZE, y))
    
    # Adicionar paredes aleatórias
    num_walls = 10 + level_num * 3
    for _ in range(num_walls):
        x = random.randint(2, WIDTH//GRID_SIZE - 3) * GRID_SIZE
        y = random.randint(2, HEIGHT//GRID_SIZE - 3) * GRID_SIZE
        if not (x < GRID_SIZE * 3 and y < GRID_SIZE * 3):
            walls.append(Wall(x, y))
    
    # Adicionar inimigos
    num_enemies = 2 + level_num
    for _ in range(num_enemies):
        while True:
            x = random.randint(2, WIDTH//GRID_SIZE - 3) * GRID_SIZE
            y = random.randint(2, HEIGHT//GRID_SIZE - 3) * GRID_SIZE
            if not any(Rect(x, y, GRID_SIZE, GRID_SIZE).colliderect(wall.get_rect()) for wall in walls):
                if math.hypot(player.x - x, player.y - y) > GRID_SIZE * 5:
                    enemies.append(Enemy(x, y))
                    break
    
    # Adicionar tesouros
    num_treasures = 3 + level_num
    for _ in range(num_treasures):
        while True:
            x = random.randint(2, WIDTH//GRID_SIZE - 3) * GRID_SIZE
            y = random.randint(2, HEIGHT//GRID_SIZE - 3) * GRID_SIZE
            test_rect = Rect(x, y, GRID_SIZE, GRID_SIZE)
            if (not any(test_rect.colliderect(wall.get_rect()) for wall in walls) and
                not any(test_rect.colliderect(enemy.get_rect()) for enemy in enemies)):
                treasures.append(Treasure(x, y))
                break

def start_game():
    global game_state, score, level
    game_state = "playing"
    score = 0
    level = 1
    generate_level(level)
    if audio_enabled:
        sounds.background.play(-1)

def update():
    global animation_timer, score, game_state, level
    
    animation_timer += 1
    
    if game_state == "menu":
        mouse_pos = (0, 0)
        try:
            mouse_pos = pygame.mouse.get_pos()
            start_button.check_hover(mouse_pos)
            audio_button.check_hover(mouse_pos)
            exit_button.check_hover(mouse_pos)
        except:
            pass
    
    elif game_state == "playing":
        player.update()
        for enemy in enemies:
            enemy.update()
        
        # Verificar conclusão do nível
        if not treasures:
            level += 1
            generate_level(level)

def draw():
    screen.clear()
    
    if game_state == "menu":
        # Desenhar menu
        screen.fill((20, 20, 40))
        screen.draw.text("DUNGEON EXPLORER", centerx=WIDTH//2, centery=HEIGHT//4, 
                         fontsize=50, color=(255, 255, 255))
        screen.draw.text("Use as setas para mover, colete tesouros, evite inimigos",
                         centerx=WIDTH//2, centery=HEIGHT//3, fontsize=20, color=(200, 200, 200))
        start_button.draw()
        audio_button.draw()
        exit_button.draw()
        if high_score > 0:
            screen.draw.text(f"Recorde: {high_score}", centerx=WIDTH//2, centery=HEIGHT*4//5,
                           fontsize=20, color=(255, 255, 100))
    
    elif game_state in ("playing", "game_over"):
        # Desenhar o jogo
        for y in range(0, HEIGHT, GRID_SIZE):
            for x in range(0, WIDTH, GRID_SIZE):
                screen.blit(images.floor, (x, y))
                
        for wall in walls: wall.draw()
        for treasure in treasures: treasure.draw()
        for enemy in enemies: enemy.draw()
        
        if player.invulnerable_timer <= 0 or animation_timer % 4 < 2:
            player.draw()
            
        screen.draw.text(f"Pontuação: {score}", (10, 10), fontsize=20, color=(255, 255, 255))
        screen.draw.text(f"Nível: {level}", (10, 40), fontsize=20, color=(255, 255, 255))
        
        if game_state == "game_over":
            screen.draw.filled_rect(Rect(WIDTH//4, HEIGHT//3, WIDTH//2, HEIGHT//3), (0, 0, 0, 180))
            screen.draw.text("FIM DE JOGO", centerx=WIDTH//2, centery=HEIGHT//2 - 40,
                           fontsize=40, color=(255, 50, 50))
            screen.draw.text(f"Pontuação final: {score}", centerx=WIDTH//2, centery=HEIGHT//2,
                           fontsize=30, color=(255, 255, 255))
            screen.draw.text("Pressione ENTER para jogar novamente", centerx=WIDTH//2, 
                           centery=HEIGHT//2 + 40, fontsize=20, color=(200, 200, 200))

def on_mouse_down(pos, button):
    global game_state, audio_enabled
    
    if game_state == "menu":
        if start_button.check_click(pos):
            start_game()
        elif audio_button.check_click(pos):
            audio_enabled = not audio_enabled
            audio_button.text = f"Som: {'ON' if audio_enabled else 'OFF'}"
            if audio_enabled:
                sounds.background.play(-1)
            else:
                sounds.background.stop()
        elif exit_button.check_click(pos):
            exit()

def on_key_down(key):
    global game_state, score, level
    
    if game_state == "menu" and key == keys.RETURN:
        start_game()
    elif game_state == "game_over" and key == keys.RETURN:
        score = 0
        level = 1
        game_state = "playing"
        generate_level(level)

# Inicialização do jogo
generate_level(level)
pgzrun.go()