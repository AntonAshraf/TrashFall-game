import random
import pygame


# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BIN_SIZE = 80
TRASH_SIZE = 20
TRASH_SPEED = 5
CLOUD_SPEED = 2
FLOWER_RADIUS = 5
TREE_HEIGHT = 50
TREE_WIDTH = 20

# Global variables
bin_x = WINDOW_WIDTH // 2
trash_x = random.randint(0, WINDOW_WIDTH)
trash_y = WINDOW_HEIGHT
score = 0
lives = 3
game_over = False
clouds = []
flowers = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT // 4)) for _ in range(10)]
trees = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT // 4)) for _ in range(5)]
sliding_text_offset = 1  # Offset for sliding text

# Play background music
pygame.mixer.init()
background_music = pygame.mixer.Sound("assets/background.mp3")
game_over_sound = pygame.mixer.Sound("assets/gameover.mp3")
trash_sound = pygame.mixer.Sound("assets/trash.mp3")
trash2_sound = pygame.mixer.Sound("assets/trash2.mp3")
trash3_sound = pygame.mixer.Sound("assets/trash3.mp3")
collect = pygame.mixer.Sound("assets/collect.mp3")
yay = pygame.mixer.Sound("assets/yay.mp3")
background_music.set_volume(0.5)
background_music.play(-1)

# Variable to track if the game is running
game_running = False