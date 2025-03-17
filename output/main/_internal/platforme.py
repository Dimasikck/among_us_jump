import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

class Platform:
    def __init__(self, x, y, width, height, image_path=None, moving=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.moving = moving
        self.moving_speed = 2
        self.moving_direction = 1
        self.moving_bounds = (0, SCREEN_WIDTH)
        self.player_on_platform = False  # Добавляем флаг, чтобы отслеживать игрока
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def check_collision(self, player_rect, player_velocity):
        if self.rect.colliderect(player_rect):
            if player_velocity > 0 and player_rect.bottom >= self.rect.top and player_rect.bottom <= self.rect.centery:
                return True
        return False

    def update(self, player_rect=None, dt=None):
        if self.moving is not None:
            self.x += self.moving_direction * self.moving_speed
            if self.x <= self.moving_bounds[0] or self.x + self.width >= self.moving_bounds[1]:
                self.moving_direction *= -1
            self.update_rect()

        # Устанавливаем флаг, если игрок находится на платформе
        if player_rect and self.check_collision(player_rect, 1):
            self.player_on_platform = True
        else:
            self.player_on_platform = False


class FallingPlatform(Platform):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height, image_path)
        self.fall_time = 0
        self.falling = False
        self.fall_speed = 10

    def update(self, player_rect, dt):
        # Обновляем флаг на основе проверки столкновения с игроком
        if player_rect and self.check_collision(player_rect, 1):
            self.player_on_platform = True
        else:
            self.player_on_platform = False

        if not self.falling and self.player_on_platform:
            self.fall_time += dt
            if self.fall_time >= 4000:
                self.falling = True

        if self.falling:
            self.y += self.fall_speed
            if self.y > SCREEN_HEIGHT:
                self.y = SCREEN_HEIGHT + self.height  # Убедимся, что платформа удалена с экрана
        self.update_rect()