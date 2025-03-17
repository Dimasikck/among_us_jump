
import pygame
from settings import *
from assets import load_player_frames
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.jump_speed = JUMP_SPEED
        self.gravity = GRAVITY
        self.is_jumping = False
        self.jump_velocity = 0
        self.on_platform = False
        self.was_on_platform = False
        self.frames = load_player_frames()
        self.current_frame = 0
        self.frame_rate = 12
        self.last_update_time = pygame.time.get_ticks()
        self.last_direction = 'right'
        self.running_sound_playing = False
        self.run_sound = pygame.mixer.Sound('assets/sounds/running.mp3')
        self.jump_sound = pygame.mixer.Sound('assets/sounds/jumping.mp3')
        self.land_sound = pygame.mixer.Sound('assets/sounds/jumping.mp3')
        self.jetpack_sound = pygame.mixer.Sound('assets/sounds/jetpack.mp3')
        self.jetpack_sound.set_volume(0.2)
        self.jetpack_sound_playing = False
        self.moving = False
        self.jump_delay = 700  # Задержка в миллисекундах
        self.last_jump_time = 0  # Время последнего прыжка
        self.image = self.frames['right'][0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.on_moving_platform = False
        self.platform = None

    def handle_keys(self, keys):
        self.moving = False
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.rect.x = self.x  # обновляем позицию rect
            self.last_direction = 'left'
            self.moving = True
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.rect.x = self.x  # обновляем позицию rect
            self.last_direction = 'right'
            self.moving = True
        if not self.is_jumping:
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and (current_time - self.last_jump_time >= self.jump_delay):
                self.is_jumping = True
                self.on_platform = False
                self.jump_velocity = -self.jump_speed
                self.jump_sound.play()
                self.jetpack_sound.play(-1)  # Проигрываем звук джекпака в цикле
                self.jetpack_sound_playing = True
                self.last_jump_time = current_time  # Обновляем время последнего прыжка

    def handle_jumping(self, platforms):
        if self.is_jumping:
            self.y += self.jump_velocity
            self.rect.y = self.y  # обновляем позицию rect
            self.jump_velocity += self.gravity

            for platform in platforms:
                if platform.check_collision(self.get_rect(), self.jump_velocity):
                    self.y = platform.y - self.height
                    self.rect.y = self.y  # обновляем позицию rect
                    self.is_jumping = False
                    self.on_platform = True
                    self.jump_velocity = 0
                    if platform.moving:
                        self.on_moving_platform = True
                        self.platform = platform
                    else:
                        self.on_moving_platform = False
                        self.platform = None
                    if not self.was_on_platform:  # Проверяем был ли уже на платформе
                        self.land_sound.play()
                    self.stop_jetpack_sound()
                    self.was_on_platform = True
                    platform.start_time = pygame.time.get_ticks()  # Устанавливаем время нахождения игрока на платформе
                    break
        else:
            self.was_on_platform = self.check_on_platform(platforms)
            if self.was_on_platform:

                self.stop_jetpack_sound()

    def update(self, platforms):
        if not self.is_jumping and not self.check_on_platform(platforms):
            self.is_jumping = True
            self.jump_velocity = self.gravity

        self.handle_jumping(platforms)
        self.check_screen_edges()
        self.update_frame()
        self.update_sounds()

        # Двигаем игрока вместе с платформой, если он на движущейся платформе
        if self.on_moving_platform and self.platform:
            self.x += self.platform.moving_direction * self.platform.moving_speed
            self.rect.x = self.x  # обновляем позицию rect
    def stop_jetpack_sound(self):
        if self.jetpack_sound_playing:
            self.jetpack_sound.stop()
            self.jetpack_sound_playing = False

    def check_on_platform(self, platforms):
        for platform in platforms:
            if platform.check_collision(self.get_rect(), 0):
                return True
        return False

    def check_screen_edges(self):
        if self.x < -self.width:
            self.x = SCREEN_WIDTH
            self.rect.x = self.x  # обновляем позицию rect
        elif self.x > SCREEN_WIDTH:
            self.x = -self.width
            self.rect.x = self.x  # обновляем позицию rect

    def update_frame(self):
        current_time = pygame.time.get_ticks()
        if self.moving:
            if current_time - self.last_update_time > 1000 // self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.last_direction])
                self.last_update_time = current_time
        else:
            self.current_frame = 0

    def update_sounds(self):
        if self.moving and not self.is_jumping:
            if not self.running_sound_playing:
                self.run_sound.play(-1)  # Play sound in a loop
                self.running_sound_playing = True
        else:
            if self.running_sound_playing:
                self.run_sound.stop()
                self.running_sound_playing = False

    def draw(self, screen):
        if self.is_jumping:
            screen.blit(self.frames['jump'][self.last_direction][0], (self.x, self.y))
        else:
            screen.blit(self.frames[self.last_direction][self.current_frame], (self.x, self.y))

    def get_rect(self):
        return self.rect

