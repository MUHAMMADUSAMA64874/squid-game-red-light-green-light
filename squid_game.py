import pygame
import sys
import random
import pyttsx3

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load sound effects
pygame.mixer.music.load("effects/background_music.mp3")  # Add background music
coin_sound = pygame.mixer.Sound("effects/coin_collect.mp3")  # Add coin collection sound
game_over_sound = pygame.mixer.Sound("effects/game_over.wav")  # Add game over sound
win_sound = pygame.mixer.Sound("effects/win_sound.mp3")  # Add win sound
menu_sound = pygame.mixer.Sound("effects/menu_select.mp3")  # Add menu sound

# Function to play text sound
def play_text_sound(text):
    engine.say(text)
    engine.runAndWait()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Squid Game: Red Light, Green Light - Level 1")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
PINK = (200, 0, 100)
DARK_GRAY = (30, 30, 30)

# Fonts
font = pygame.font.Font(None, 36)

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 20

# Game states
MAIN_MENU = 0
INSTRUCTIONS = 1
PLAYING = 2
GAME_OVER = 3
WIN_SCREEN = 4
current_state = MAIN_MENU

# Timer and lives
PLAYER_LIVES = 3
LEVEL_TIMER = 60

# Pixel art for player, bots, and coins
PLAYER_PIXELS = [
    [0, 0, 1, 1, 0, 0],
    [0, 1, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 1],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0],
]

BOT_PIXELS = [
    [0, 0, 3, 3, 0, 0],
    [0, 3, 4, 4, 3, 0],
    [3, 4, 4, 4, 4, 3],
    [3, 4, 4, 4, 4, 3],
    [0, 3, 3, 3, 3, 0],
    [0, 3, 3, 3, 3, 0],
]

COIN_PIXELS = [
    [0, 0, 5, 5, 0, 0],
    [0, 5, 5, 5, 5, 0],
    [5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5],
    [0, 5, 5, 5, 5, 0],
    [0, 0, 5, 5, 0, 0],
]

COLOR_MAP = {
    0: BLACK,
    1: BLUE,
    2: WHITE,
    3: RED,
    4: WHITE,
    5: YELLOW,
}

# Pixel art for Evil Laugh Intro
mask_pixels = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 3, 3, 2, 2, 1],
    [0, 1, 2, 3, 3, 2, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]

# Pixel art for Game Over screen
game_over_pixels = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 3, 3, 2, 2, 1],
    [1, 2, 2, 3, 3, 2, 2, 1],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]

# Pixel art for Winning screen
win_pixels = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 4, 4, 2, 2, 1],
    [1, 2, 2, 4, 4, 2, 2, 1],
    [0, 1, 2, 2, 2, 2, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0],
]

pixel_size = 20  # Size of each pixel in the grid

# Function to draw pixel art
def draw_pixel_art(surface, x, y, pixels, color_map):
    for row_idx, row in enumerate(pixels):
        for col_idx, pixel in enumerate(row):
            if pixel in color_map:
                pygame.draw.rect(surface, color_map[pixel], (x + col_idx * pixel_size, y + row_idx * pixel_size, pixel_size, pixel_size))

# Player class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vel_y = 0
        self.on_ground = False
        self.score = 0
        self.lives = PLAYER_LIVES
        self.red_light_moves = 0  # Track red light moves

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.on_ground = False

    def update(self):
        self.vel_y += GRAVITY
        self.move(0, self.vel_y)

        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True

    def draw(self):
        for row in range(len(PLAYER_PIXELS)):
            for col in range(len(PLAYER_PIXELS[row])):
                color = COLOR_MAP[PLAYER_PIXELS[row][col]]
                if color != BLACK:
                    pygame.draw.rect(
                        screen,
                        color,
                        (
                            self.rect.x + col * 5,
                            self.rect.y + row * 5,
                            5,
                            5,
                        ),
                    )

# Bot class
class Bot:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vel_y = 0
        self.on_ground = True

    def move(self):
        self.rect.x += random.choice([-1, 1]) * PLAYER_SPEED
        if random.random() < 0.1 and self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.on_ground = False

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True

    def draw(self):
        for row in range(len(BOT_PIXELS)):
            for col in range(len(BOT_PIXELS[row])):
                color = COLOR_MAP[BOT_PIXELS[row][col]]
                if color != BLACK:
                    pygame.draw.rect(
                        screen,
                        color,
                        (
                            self.rect.x + col * 5,
                            self.rect.y + row * 5,
                            5,
                            5,
                        ),
                    )

# Coin class
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False
        self.timer = 0

    def draw(self):
        if not self.collected:
            for row in range(len(COIN_PIXELS)):
                for col in range(len(COIN_PIXELS[row])):
                    color = COLOR_MAP[COIN_PIXELS[row][col]]
                    if color != BLACK:
                        pygame.draw.rect(
                            screen,
                            color,
                            (
                                self.rect.x + col * 3,
                                self.rect.y + row * 3,
                                3,
                                3,
                            ),
                        )

    def update(self):
        if self.collected:
            self.timer += 1
            if self.timer >= 180:  # Reappear after 3 seconds
                self.collected = False
                self.timer = 0

# Red Light, Green Light game logic
class RedLightGreenLight:
    def __init__(self):
        self.state = "GREEN"
        self.timer = 0
        self.duration = random.randint(2, 5)

    def update(self):
        self.timer += 1
        if self.timer >= self.duration * 60:
            self.timer = 0
            self.state = "RED" if self.state == "GREEN" else "GREEN"
            self.duration = random.randint(2, 5)
            if self.state == "GREEN":
                play_text_sound("green light")
            else:
                play_text_sound("red light")

    def draw(self):
        color = GREEN if self.state == "GREEN" else RED
        pygame.draw.circle(screen, color, (SCREEN_WIDTH // 2, 100), 50)

# Function to draw the ground
def draw_ground():
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

# Main menu
def draw_main_menu(selected_index):
    screen.fill(BLACK)
    title = font.render("Squid Game: Red Light, Green Light", True, WHITE)
    menu_items = ["Start Game", "Instructions", "Exit"]

    # Draw menu on the left side (50%)
    for i, item in enumerate(menu_items):
        color = YELLOW if i == selected_index else WHITE
        text = font.render(item, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 4, 200 + i * 100))
        screen.blit(text, text_rect)

    # Draw pixel art on the right side (50%)
    draw_pixel_art(screen, SCREEN_WIDTH // 2, 100, mask_pixels, COLOR_MAP)

# Instructions screen
def draw_instructions():
    screen.fill(BLACK)
    instructions = [
        "Red Light, Green Light:",
        "Move when the light is GREEN.",
        "Stop when the light is RED.",
        "Use LEFT and RIGHT arrows to move.",
        "Press SPACE to jump.",
        "Collect 10 coins to win!",
        "You have 3 lives.",
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 50 + i * 40))

    back_button = font.render("Back to Menu (M)", True, WHITE)
    screen.blit(back_button, (SCREEN_WIDTH // 2 - back_button.get_width() // 2, 500))

# Game over screen
def draw_game_over(score):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    retry_button = font.render("Retry (R)", True, WHITE)
    menu_button = font.render("Back to Menu (M)", True, WHITE)

    # Draw pixel art for Game Over screen
    draw_pixel_art(screen, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 250, game_over_pixels, COLOR_MAP)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
    screen.blit(retry_button, (SCREEN_WIDTH // 2 - retry_button.get_width() // 2, 300))
    screen.blit(menu_button, (SCREEN_WIDTH // 2 - menu_button.get_width() // 2, 400))

# Winning screen
def draw_win_screen(score):
    screen.fill(BLACK)
    win_text = font.render("You Won!", True, GREEN)
    score_text = font.render(f"Score: {score}", True, WHITE)
    retry_button = font.render("Retry (R)", True, WHITE)
    menu_button = font.render("Back to Menu (M)", True, WHITE)

    # Draw pixel art for Winning screen
    draw_pixel_art(screen, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 250, win_pixels, COLOR_MAP)

    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
    screen.blit(retry_button, (SCREEN_WIDTH // 2 - retry_button.get_width() // 2, 300))
    screen.blit(menu_button, (SCREEN_WIDTH // 2 - menu_button.get_width() // 2, 400))

# Main game loop
def main():
    global current_state

    # Initialize game objects
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    bots = [Bot(random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH), SCREEN_HEIGHT - 100) for _ in range(5)]
    coins = [Coin(random.randint(0, SCREEN_WIDTH - 20), random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 100)) for _ in range(10)]
    red_light_green_light = RedLightGreenLight()
    clock = pygame.time.Clock()
    selected_menu_index = 0  # For main menu navigation

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle menu navigation
            if current_state == MAIN_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_menu_index = (selected_menu_index + 1) % 3
                        menu_sound.play()
                    elif event.key == pygame.K_UP:
                        selected_menu_index = (selected_menu_index - 1) % 3
                        menu_sound.play()
                    elif event.key == pygame.K_RETURN:
                        if selected_menu_index == 0:
                            current_state = PLAYING
                            pygame.mixer.music.play(-1)  # Start background music
                        elif selected_menu_index == 1:
                            current_state = INSTRUCTIONS
                        elif selected_menu_index == 2:
                            pygame.quit()
                            sys.exit()

            # Handle game over and win screen navigation
            if current_state == GAME_OVER or current_state == WIN_SCREEN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        current_state = PLAYING
                        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
                        bots = [Bot(random.randint(0, SCREEN_WIDTH - PLAYER_WIDTH), SCREEN_HEIGHT - 100) for _ in range(5)]
                        coins = [Coin(random.randint(0, SCREEN_WIDTH - 20), random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 100)) for _ in range(10)]
                        pygame.mixer.music.play(-1)  # Start background music
                    elif event.key == pygame.K_m:
                        current_state = MAIN_MENU

            # Handle instructions screen navigation
            if current_state == INSTRUCTIONS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        current_state = MAIN_MENU

            # Handle player movement during gameplay
            if current_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()

        # Update game objects based on current state
        if current_state == PLAYING:
            keys = pygame.key.get_pressed()
            if red_light_green_light.state == "GREEN":
                if keys[pygame.K_LEFT]:
                    player.move(-PLAYER_SPEED, 0)
                if keys[pygame.K_RIGHT]:
                    player.move(PLAYER_SPEED, 0)
            else:
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                    player.red_light_moves += 1
                    if player.red_light_moves > 3:
                        player.lives -= 1
                        player.red_light_moves = 0
                        if player.lives == 2:
                            play_text_sound("2 lives left")
                        elif player.lives == 1:
                            play_text_sound("1 life left")
                        elif player.lives <= 0:
                            current_state = GAME_OVER
                            pygame.mixer.music.stop()
                            game_over_sound.play()

            player.update()
            for bot in bots:
                bot.move()
            red_light_green_light.update()

            # Check for coin collection
            for coin in coins:
                if not coin.collected and player.rect.colliderect(coin.rect):
                    coin.collected = True
                    player.score += 1
                    coin_sound.play
                if player.score >= 10:  # Win condition
                        current_state = WIN_SCREEN
                        pygame.mixer.music.stop()
                        win_sound.play()

            # Update coins
            for coin in coins:
                coin.update()

        # Draw the screen based on the current state
        screen.fill(BLACK)

        if current_state == MAIN_MENU:
            draw_main_menu(selected_menu_index)
        elif current_state == INSTRUCTIONS:
            draw_instructions()
        elif current_state == PLAYING:
            draw_ground()
            player.draw()
            for bot in bots:
                bot.draw()
            for coin in coins:
                coin.draw()
            red_light_green_light.draw()

            # Display player stats
            lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
            score_text = font.render(f"Score: {player.score}", True, WHITE)
            screen.blit(lives_text, (10, 10))
            screen.blit(score_text, (10, 50))
        elif current_state == GAME_OVER:
            draw_game_over(player.score)
        elif current_state == WIN_SCREEN:
            draw_win_screen(player.score)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Run the game
if __name__ == "__main__":
    main()
