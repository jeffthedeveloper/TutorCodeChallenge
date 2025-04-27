import pgzrun
import random
from pygame import Rect
import pygame

# Configurações
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 30
PLAYER_SPEED = 1.5
ENEMY_SPEED = 0.7
TITLE = "Dungeon Mini"

# Estados do jogo
game_state = "menu"
score = 0
music_enabled = True
sound_effects_enabled = True
level = 1

# Objetos
player_pos = [WIDTH // 2, HEIGHT // 2]
enemies = []
treasures = []
walls = []

# Menu
menu_options = ["Começar Jogo", "Música: ON", "Sair"]
menu_index = 0


# Botão de som no jogo
sound_button_rect = Rect(WIDTH - 110, 10, 100, 20)

# Carregar sons
try:
    pygame.mixer.init()
    sounds.background = pygame.mixer.Sound('music/background.ogg')
    sounds.hit = pygame.mixer.Sound('sounds/hit.ogg')
    sounds.pickup = pygame.mixer.Sound('sounds/pickup.ogg')
except pygame.error as e:
    print(f"Erro ao carregar sons: {e}")
    sounds.background = None
    sounds.hit = None
    sounds.pickup = None


def generate_level():
    global player_pos, enemies, treasures, walls
    player_pos = [WIDTH // 2, HEIGHT // 2]
    num_enemies = 2 + level // 2
    enemies = [[random.uniform(GRID_SIZE, WIDTH - GRID_SIZE), random.uniform(GRID_SIZE, HEIGHT - GRID_SIZE),
                random.choice([-1, 1]), random.choice([-1, 1]), random.randint(30, 60)] for _ in range(num_enemies)]
    num_treasures = 3 + level // 3
    treasures = [[random.randrange(1, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                  random.randrange(1, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE] for _ in range(num_treasures)]
    walls = []
    num_walls = 8 + level // 4
    for _ in range(num_walls):
        x = random.randrange(1, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randrange(1, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        walls.append([x, y])


def draw():
    screen.clear()
    if game_state == "menu":
        screen.fill((30, 30, 50))
        screen.draw.text("DUNGEON MINI", centerx=WIDTH // 2,
                         centery=HEIGHT // 2 - 60, fontsize=40, color=(255, 255, 255))
        for i, option in enumerate(menu_options):
            color = (255, 255, 255) if i == menu_index else (200, 200, 200)
            screen.draw.text(option, centerx=WIDTH // 2, centery=HEIGHT //
                             2 - 10 + i * 30, fontsize=24, color=color)
        music_text = "Música: ON" if music_enabled else "Música: OFF"

        if music_enabled and sounds.background and not pygame.mixer.get_busy():
            pygame.mixer.music.play(-1)
        elif not music_enabled and sounds.background and pygame.mixer.get_busy():
            pygame.mixer.music.stop()
    elif game_state == "playing":
        screen.draw.rect(
            Rect(player_pos[0], player_pos[1], GRID_SIZE, GRID_SIZE), (0, 128, 255))
        for enemy in enemies:
            screen.draw.rect(
                Rect(enemy[0], enemy[1], GRID_SIZE, GRID_SIZE), (255, 0, 0))
        for treasure_pos in treasures:
            screen.draw.rect(
                Rect(treasure_pos[0], treasure_pos[1], GRID_SIZE, GRID_SIZE), (255, 255, 0))
        for wall_pos in walls:
            screen.draw.rect(
                Rect(wall_pos[0], wall_pos[1], GRID_SIZE, GRID_SIZE), (100, 100, 100))
        screen.draw.text(f"Score: {score}", (10, 10), color=(255, 255, 255))
        screen.draw.text(f"Nível: {level}", (10, 30), color=(255, 255, 255))
        sounds_text = "Sons: ON" if sound_effects_enabled else "Sons: OFF"
        screen.draw.textbox(sounds_text, sound_button_rect,
                            color=(255, 255, 255), align="center")
        if sounds.background and pygame.mixer.get_busy():
            pygame.mixer.music.stop()
    elif game_state == "game_over":
        screen.fill((0, 0, 0))
        screen.draw.text("Game Over!", center=(
            WIDTH // 2, HEIGHT // 2 - 20), color=(255, 0, 0), fontsize=40)
        screen.draw.text(f"Final Score: {score}", center=(
            WIDTH // 2, HEIGHT // 2 + 20), color=(255, 255, 255), fontsize=30)
        screen.draw.text("Pressione ESPAÇO para voltar ao Menu", center=(
            WIDTH // 2, HEIGHT // 2 + 60), color=(200, 200, 200), fontsize=20)
        if music_enabled and sounds.background and not pygame.mixer.get_busy():
            pygame.mixer.music.play(-1)


def update():
    global player_pos, enemies, treasures, score, game_state, level

    if game_state == "playing":
        if keyboard.left:
            player_pos[0] -= PLAYER_SPEED
        if keyboard.right:
            player_pos[0] += PLAYER_SPEED
        if keyboard.up:
            player_pos[1] -= PLAYER_SPEED
        if keyboard.down:
            player_pos[1] += PLAYER_SPEED
        player_pos[0] = max(0, min(player_pos[0], WIDTH - GRID_SIZE))
        player_pos[1] = max(0, min(player_pos[1], HEIGHT - GRID_SIZE))

        for enemy in enemies:
            enemy[0] += enemy[2] * ENEMY_SPEED
            enemy[1] += enemy[3] * ENEMY_SPEED
            enemy[4] -= 1
            if enemy[4] <= 0:
                enemy[2] = random.choice([-1, 1])
                enemy[3] = random.choice([-1, 1])
                enemy[4] = random.randint(30, 60)
            if enemy[0] < 0 or enemy[0] > WIDTH - GRID_SIZE:
                enemy[2] *= -1
                enemy[0] = max(0, min(enemy[0], WIDTH - GRID_SIZE))
                enemy[4] = random.randint(30, 60)
            if enemy[1] < 0 or enemy[1] > HEIGHT - GRID_SIZE:
                enemy[3] *= -1
                enemy[1] = max(0, min(enemy[1], HEIGHT - GRID_SIZE))
                enemy[4] = random.randint(30, 60)

        if not treasures:
            level += 1
            generate_level()
            return

        for i, treasure_pos in enumerate(treasures[:]):
            if Rect(player_pos[0], player_pos[1], GRID_SIZE, GRID_SIZE).colliderect(Rect(treasure_pos[0], treasure_pos[1], GRID_SIZE, GRID_SIZE)):
                score += 100
                if sounds.pickup and sound_effects_enabled:
                    sounds.pickup.play()
                treasures.pop(i)
                break

        for enemy in enemies:
            if Rect(player_pos[0], player_pos[1], GRID_SIZE, GRID_SIZE).colliderect(Rect(enemy[0], enemy[1], GRID_SIZE, GRID_SIZE)):
                game_state = "game_over"
                if sounds.hit and sound_effects_enabled:
                    sounds.hit.play()
                    if sounds.background and pygame.mixer.get_busy():
                        pygame.mixer.music.stop()

        player_rect = Rect(player_pos[0], player_pos[1], GRID_SIZE, GRID_SIZE)
        for wall_pos in walls:
            if player_rect.colliderect(Rect(wall_pos[0], wall_pos[1], GRID_SIZE, GRID_SIZE)):
                if keyboard.left:
                    player_pos[0] += PLAYER_SPEED
                if keyboard.right:
                    player_pos[0] -= PLAYER_SPEED
                if keyboard.up:
                    player_pos[1] += PLAYER_SPEED
                if keyboard.down:
                    player_pos[1] -= PLAYER_SPEED
                break


def on_mouse_down(pos):
    global game_state, music_enabled, sound_effects_enabled, menu_index
    if game_state == "menu":
        if music_button_rect.collidepoint(pos):
            music_enabled = not music_enabled
            menu_options[1] = f"Música: {'ON' if music_enabled else 'OFF'}"
            if music_enabled and sounds.background and not pygame.mixer.get_busy():
                pygame.mixer.music.play(-1)
            elif not music_enabled and sounds.background and pygame.mixer.get_busy():
                pygame.mixer.music.stop()
        # Botão "Começar Jogo" (aproximado)
        elif Rect(WIDTH // 2 - 150, HEIGHT // 2 - 40, 300, 30).collidepoint(pos):
            game_state = "playing"
            level = 1
            generate_level()
            if sounds.background and pygame.mixer.get_busy():
                pygame.mixer.music.stop()
        # Botão "Sair" (aproximado)
        elif Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 30).collidepoint(pos):
            quit()
    elif game_state == "playing":
        if sound_button_rect.collidepoint(pos):
            sound_effects_enabled = not sound_effects_enabled


def on_key_down(key):
    global game_state, score, menu_index, music_enabled, level
    if game_state == "menu":
        if key == keys.UP:
            menu_index = (menu_index - 1) % len(menu_options)
        elif key == keys.DOWN:
            menu_index = (menu_index + 1) % len(menu_options)
        elif key == keys.RETURN:
            if menu_index == 0:
                game_state = "playing"
                level = 1
                generate_level()
                if sounds.background and music_enabled:
                    pygame.mixer.music.stop()
            elif menu_index == 1:
                music_enabled = not music_enabled
                menu_options[1] = f"Música: {'ON' if music_enabled else 'OFF'}"
                if music_enabled and sounds.background and not pygame.mixer.get_busy():
                    pygame.mixer.music.play(-1)
                elif not music_enabled and sounds.background and pygame.mixer.get_busy():
                    pygame.mixer.music.stop()
            elif menu_index == 2:
                quit()
    elif game_state == "game_over" and key == keys.SPACE:
        game_state = "menu"
        if sounds.background and music_enabled and not pygame.mixer.get_busy():
            pygame.mixer.music.play(-1)


# Inicialização do Pygame Mixer para música
pygame.mixer.init()
try:
    pygame.mixer.music.load('music/background.ogg')
except pygame.error as e:
    print(f"Erro ao carregar música de fundo (pygame.mixer.music): {e}")

# Inicialização do jogo
pgzrun.go()
