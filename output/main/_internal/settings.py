import pygame


pygame.init()

ICON = pygame.image.load('assets/images/icon.png')
TITLE_GAME = 'Among Us Jump'

screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


PLAYER_WIDTH = SCREEN_WIDTH // 10
PLAYER_HEIGHT = SCREEN_HEIGHT // 5

PLAYER_SPEED = 11
JUMP_SPEED = 22
GRAVITY = 1


# Списки координат для генерации платформ
PLATFORM_X_COORDS = list(range(0, SCREEN_WIDTH, SCREEN_WIDTH // 8))
PLATFORM_Y_SPACING = 150  # Расстояние между платформами по оси Y
PLATFORM_Y_START = SCREEN_HEIGHT - 200  # Начальная позиция по оси Y для платформ


BACKGROUND_IMGS = [
    pygame.transform.scale(pygame.image.load('assets/images/background.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/background2.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
]

MENU_BACKGROUND = pygame.transform.scale(pygame.image.load('assets/images/main_menu.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

SCROLL_THRESH = SCREEN_HEIGHT
MIDDLE_Y = SCREEN_HEIGHT // 2

GAME_OVER_IMG = pygame.transform.scale(pygame.image.load('assets/images/game_over.png').convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.mp3')

FONT_LARGE = pygame.font.Font(None, 134)
FONT_SMALL = pygame.font.Font(None, 66)
FONT_SCORE = pygame.font.Font(None, 56)

ENEMY_WIDTH = SCREEN_WIDTH//11
ENEMY_HEIGHT = SCREEN_HEIGHT//10


BEST_SCORE_FILE = 'best_score.txt'

pygame.mixer.music.load('assets/sounds/background_music.mp3')
pygame.mixer.music.set_volume(0.2)


