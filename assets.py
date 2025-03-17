import pygame
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT

pygame.init()

def load_player_frames():
    playerR_frame = [
    pygame.transform.scale(pygame.image.load('assets/images/player/playerR_1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/player/playerR_2.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/player/playerR_3.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/player/playerR_4.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/player/playerR_5.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
                    ]
    playerL_frame = [
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_2.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_3.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_4.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_5.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))]
    playerJR_frame = [
        pygame.transform.scale(pygame.image.load('assets/images/player/playerJR.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerR_1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
                    ]
    playerJL_frame = [
        pygame.transform.scale(pygame.image.load('assets/images/player/playerJL.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
    ]
    return {
        'right': playerR_frame,
        'left': playerL_frame,
        'jump':{
            'right': playerJR_frame,
            'left': playerJL_frame
        }
    }

def load_enemy_frames(direction):
    frames = {
        'right' : [pygame.transform.scale(pygame.image.load(f'assets/images/enemy/enemyR_{i}.png'), (ENEMY_WIDTH, ENEMY_HEIGHT)) for i in range(1,5)],
        'left' : [pygame.transform.scale(pygame.image.load(f'assets/images/enemy/enemyL_{i}.png'), (ENEMY_WIDTH, ENEMY_HEIGHT)) for i in range(1,5)]
    }
    return frames[direction]
