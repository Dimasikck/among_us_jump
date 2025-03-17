import pygame
import random
from settings import *
from assets import load_enemy_frames

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.current_frame = 0
        self.frame_rate = 10
        self.last_update_time = pygame.time.get_ticks()
        self.enemy_speed = 3
        self.direction = random.choice([-1,1])
        if self.direction == 1:
            self.frames = load_enemy_frames('right')
        else:
            self.frames = load_enemy_frames('left')
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.enemy_speed *self.direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.update_direction()
        self.update_frame()

    def update_direction(self):
        if self.direction == 1:
            self.frames = load_enemy_frames('right')
        else:
            self.frames = load_enemy_frames('left')

    def update_frame(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 1000 // self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update_time = current_time

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    def get_rect(self):
        return self.rect
