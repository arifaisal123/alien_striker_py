import pygame
import random
import os

# Initialize PyGame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images")
SOUND_PATH = os.path.join(BASE_DIR, "assets", "sounds")
DATA_PATH = os.path.join(BASE_DIR, "highscore.txt")  # File to store high scores

# Load Images with Correct Paths
player_img = pygame.image.load(os.path.join(IMAGE_PATH, "spaceship.png"))
enemy_img = pygame.image.load(os.path.join(IMAGE_PATH, "alien.png"))
bullet_img = pygame.image.load(os.path.join(IMAGE_PATH, "bullet.png"))

# Load Sounds
pygame.mixer.init()  # Initialize the sound mixer
shoot_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "shoot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "explosion.wav"))

# Display confirmation
print("Images and sounds loaded successfully!")

# Set up font
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 50)

# Load High Score
def load_high_score():
    if os.path.exists(DATA_PATH):  # Check if file exists
        with open(DATA_PATH, "r") as file:
            content = file.read().strip()
            if content.isdigit():  # Ensure it contains a valid number
                return int(content)
    return 0  # Return 0 if file is empty or invalid

# Save High Score
def save_high_score(new_score):
    high_score = load_high_score()
    if new_score > high_score:
        with open(DATA_PATH, "w") as file:
            file.write(str(new_score))

# Initialize Score
global score
score = 0
high_score = load_high_score()

# Button Function
def draw_button(text, x, y):
    button_rect = pygame.Rect(x, y, 200, 50)
    pygame.draw.rect(screen, WHITE, button_rect, border_radius=10)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + 100, y + 25))
    screen.blit(text_surface, text_rect)
    return button_rect

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 60)
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 7  # Move bullet upwards
        if self.rect.bottom < 0:
            self.kill()  # Remove bullet when off-screen

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 4)

    def update(self):
        global running, score
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:  # If enemy reaches the bottom, game over
            print("Game Over!")  # Debugging
            save_high_score(score)  # Save high score before quitting
            score = 0  # Reset the score
            running = False  # End the game

# Function to Draw Score
def draw_score():
    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Main Menu
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)

        # Draw title
        title_text = title_font.render("SPACE SHOOTER", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Draw buttons
        start_button = draw_button("Start Game", WIDTH // 2 - 100, 200)
        how_to_play_button = draw_button("How to Play", WIDTH // 2 - 100, 270)
        high_score_button = draw_button("High Scores", WIDTH // 2 - 100, 340)
        exit_button = draw_button("Exit", WIDTH // 2 - 100, 410)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                if how_to_play_button.collidepoint(event.pos):
                    show_how_to_play()
                if high_score_button.collidepoint(event.pos):
                    show_high_scores()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# How to Play Screen
def show_how_to_play():
    how_running = True
    while how_running:
        screen.fill(BLACK)
        instructions = [
            "HOW TO PLAY",
            "Move Left: Left Arrow",
            "Move Right: Right Arrow",
            "Shoot: Spacebar",
            "Destroy enemies to score points!",
            "Press any key to go back"
        ]
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 150 + i * 40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

# High Score Screen
def show_high_scores():
    high_running = True
    while high_running:
        screen.fill(BLACK)
        high_text = font.render(f"High Score: {load_high_score()}", True, WHITE)
        screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

# Game Over Screen
def game_over_screen():
    global score
    save_high_score(score)
    while True:
        screen.fill(BLACK)
        game_over_text = title_font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))

        score_text = font.render(f"Your Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))

        restart_button = draw_button("Restart", WIDTH // 2 - 100, 450)
        exit_button = draw_button("Exit", WIDTH // 2 - 100, 520)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    start_game()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Victory Screen
def victory_screen():
    global score
    save_high_score(score)
    while True:
        screen.fill(BLACK)
        congrats_text = title_font.render("CONGRATULATIONS!", True, WHITE)
        screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, 200))

        score_text = font.render(f"Your Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))

        restart_button = draw_button("Restart", WIDTH // 2 - 100, 450)
        exit_button = draw_button("Exit", WIDTH // 2 - 100, 520)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    start_game()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Start the Game
def start_game():
    global score
    score = 0
    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    for _ in range(6):
        enemies.add(Enemy())

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)

    clock = pygame.time.Clock()
    while True:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        player.move(keys)
        bullets.update()
        enemies.update()

        if len(enemies) == 0:
            victory_screen()

        all_sprites.draw(screen)
        draw_score()
        pygame.display.update()
        clock.tick(60)

# Game Loop
main_menu()

# Game Setup
# player = Player()
# bullets = pygame.sprite.Group()
# enemies = pygame.sprite.Group()
# for _ in range(6):  # Create 6 enemies
#     enemies.add(Enemy())

# all_sprites = pygame.sprite.Group()
# all_sprites.add(player)
# all_sprites.add(enemies)

# running = True
# clock = pygame.time.Clock()

# # Main Game Loop
# while running:
#     screen.fill(BLACK)
#     keys = pygame.key.get_pressed()
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#             if event.key == pygame.K_SPACE:  # Shoot bullet
#                 bullet = Bullet(player.rect.centerx, player.rect.top)
#                 bullets.add(bullet)
#                 all_sprites.add(bullet)

#                 # Play shooting sound
#                 shoot_sound.play()

#     # Update objects
#     player.move(keys)
#     bullets.update()
#     enemies.update()

#     # Collision Detection & Score Update
#     # global score
#     for bullet in bullets:
#         hit = pygame.sprite.spritecollide(bullet, enemies, True)  # True removes enemy
#         if hit:
#             score += 10  # Increase score by 10 per enemy destroyed
#             bullet.kill()
#             enemies.add(Enemy())  # Spawn a new enemy

#             # Play explosion sound
#             explosion_sound.play()

#     # Draw objects
#     all_sprites.draw(screen)
    
#     # Draw Score
#     draw_score()

#     pygame.display.update()
#     clock.tick(60)  # 60 FPS

pygame.quit()
