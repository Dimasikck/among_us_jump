import pygame
import random
import asyncio
import os
from settings import *
from player import Player
from platforme import Platform, FallingPlatform
from enemies import Enemy

pygame.init()

pygame.display.set_caption(TITLE_GAME)
pygame.display.set_icon(ICON)

pygame.mixer.music.play(-1)
# Глобальные переменные
platforms = []
player = None
enemies = pygame.sprite.Group()
game_state = 'menu'
running = True
bg_scroll = 0
first_bg_scrolled = False
game_over = False
pause = False
score = 0
best_score = 0
# Загрузка лучшего счета
# def load_best_score():
#     if os.path.exists(BEST_SCORE_FILE):
#         with open(BEST_SCORE_FILE, 'r') as file:
#             return int(file.read())
#     return 0

# Сохранение лучшего счета
# def save_best_score(best_score):
#     with open(BEST_SCORE_FILE, 'w') as file:
#         file.write(str(best_score))



def generate_platform(existing_platforms, x_coords, y):
    width = random.randint(SCREEN_WIDTH // 7, SCREEN_WIDTH // 5)
    new_platform_x = random.choice(x_coords)
    new_platform_rect = pygame.Rect(new_platform_x, y, width, SCREEN_HEIGHT // 6)

    for _ in range(10):  # Максимум 10 попыток на генерацию платформы
        if not any(pygame.Rect(p.x, p.y, p.width, p.height).colliderect(new_platform_rect) for p in existing_platforms):
            break
        new_platform_x = random.choice(x_coords)
        new_platform_rect = pygame.Rect(new_platform_x, y, width, SCREEN_HEIGHT // 6)

    if random.choice([True, False]):
        moving = random.choice([None, True])
        new_platform = Platform(new_platform_x, y, width, SCREEN_HEIGHT // 6, 'assets/images/platforms/platform.png', moving=moving)
    else:
        new_platform = FallingPlatform(new_platform_x, y, width, SCREEN_HEIGHT // 6, 'assets/images/platforms/falling_platform.png')

    return new_platform



def draw_bg(bg_scroll, first_bg_scrolled):
    if first_bg_scrolled:
        screen.blit(BACKGROUND_IMGS[1], (0, bg_scroll))
        screen.blit(BACKGROUND_IMGS[1], (0, -SCREEN_HEIGHT + bg_scroll))
    else:
        screen.blit(BACKGROUND_IMGS[0], (0, bg_scroll))
        screen.blit(BACKGROUND_IMGS[1], (0, -SCREEN_HEIGHT + bg_scroll))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_score(score):
    score_surface = FONT_SCORE.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

def draw_best_score(best_score):
    best_score_surface = FONT_SCORE.render(f'Best score: {best_score}', True, (255, 255, 255))
    screen.blit(best_score_surface, (SCREEN_WIDTH - best_score_surface.get_width() - 10, 10))

def draw_pause():
    draw_text('PAUSE', FONT_LARGE, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text('Press ESC to continue game | Press R to restart game | Press E to exit main menu', FONT_SMALL, (255, 255, 255), screen,
              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60)

def draw_game_over():
    screen.blit(GAME_OVER_IMG, (0, 0))
    draw_text('Game Over', FONT_LARGE, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 100)
    draw_text(f'Score: {score}', FONT_SMALL, (255, 255, 255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(f'Best score: {best_score}', FONT_SMALL, (255, 255, 255), screen, SCREEN_WIDTH // 2,
              SCREEN_HEIGHT // 4 + 60)
    draw_text('Press R to Restart game', FONT_SMALL, (255, 255, 255), screen, SCREEN_WIDTH // 2,
              SCREEN_HEIGHT // 4 + 120)

def draw_main_menu():
    screen.blit(MENU_BACKGROUND, (0, 0))

    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 1.6 - 50, 600, 100)
    # exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 1.3 - 25, 600, 100)
    pygame.draw.rect(screen, (0, 0, 0), start_button_rect)
    # pygame.draw.rect(screen, (0, 0, 0), exit_button_rect)
    draw_text('START GAME', FONT_LARGE, (255, 255, 255), screen, start_button_rect.centerx, start_button_rect.centery)
    # draw_text('EXIT', FONT_LARGE, (255, 255, 255), screen, exit_button_rect.centerx, exit_button_rect.centery)
    pygame.display.update()
    return start_button_rect

def handle_menu_events(start_button_rect):
    global game_state, running
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        #     running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_state = 'playing'
                restart_game()
            # if event.key == pygame.K_ESCAPE:
            #     running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_button_rect.collidepoint(mouse_pos):
                    game_state = 'playing'
                    restart_game()
                # elif exit_button_rect.collidepoint(mouse_pos):
                #     running = False




def restart_game():
    global platforms, player, bg_scroll, first_bg_scrolled, game_over, score, pause, enemies
    main_platform = Platform(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 40)
    platforms = [main_platform]
    for i in range(1, 6):
        y = PLATFORM_Y_START - i * PLATFORM_Y_SPACING
        platforms.append(generate_platform(platforms, PLATFORM_X_COORDS, y))
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - (PLAYER_HEIGHT + 80))
    bg_scroll = 0
    first_bg_scrolled = False
    game_over = False
    score = 0
    pause = False
    pygame.mixer.music.play(-1)
    enemies = pygame.sprite.Group()

    generate_enemies()


def generate_enemy(existing_enemies):
    enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemy_y = random.randint(-SCREEN_HEIGHT, -SCREEN_HEIGHT // 2)
    new_enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)

    # Проверка на пересечение с существующими врагами и игроком
    while any(pygame.Rect(e.rect.x, e.rect.y, e.rect.width, e.rect.height).colliderect(new_enemy_rect) for e in
              existing_enemies) or (
            new_enemy_rect.y < player.y + PLAYER_HEIGHT and new_enemy_rect.y + ENEMY_HEIGHT > player.y):
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        enemy_y = random.randint(-SCREEN_HEIGHT, -SCREEN_HEIGHT // 2)
        new_enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)

    new_enemy = Enemy(enemy_x, enemy_y)
    return new_enemy

def generate_enemies():
    global platforms, player, bg_scroll, first_bg_scrolled, game_over, score, pause, enemies
    num_enemies = random.randint(1, 3)
    for _ in range(num_enemies):
        new_enemy = generate_enemy(enemies)
        enemies.add(new_enemy)

def check_collision(player, enemies):
    if pygame.sprite.spritecollideany(player, enemies):
        return True
    return False
main_platform = Platform(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 40)
platforms = [main_platform]
for i in range(1, 6):
    y = PLATFORM_Y_START - i * PLATFORM_Y_SPACING
    platforms.append(generate_platform(platforms, PLATFORM_X_COORDS, y))

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - (PLAYER_HEIGHT + 80))
enemies = pygame.sprite.Group()
game_state = 'menu'
running = True
clock = pygame.time.Clock()
bg_scroll = 0
first_bg_scrolled = False
game_over = False
pause = False
score = 0
score_checkpoint = 1000
best_score = 0
async def main():
    global running, game_state, best_score, platforms, player, bg_scroll, first_bg_scrolled, game_over, score, pause, enemies,score_checkpoint


    while running:
        dt = clock.tick(60)  # Установка FPS и расчет времени в мс
        if game_state == 'menu':
            start_button_rect = draw_main_menu()
            handle_menu_events(start_button_rect)
        if game_state == 'playing':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not game_over:
                            pause = not pause
                            if pause:
                                player.jetpack_sound.stop()
                                player.run_sound.stop()
                            else:
                                if not player.on_platform:
                                    player.jetpack_sound.play()
                    if event.key == pygame.K_e and pause:
                        game_state = 'menu'
                    if event.key == pygame.K_r and (game_over or pause):
                        restart_game()

            if not game_over:
                if pause:
                    draw_pause()
                else:
                    draw_bg(bg_scroll, first_bg_scrolled)

                    for platform in platforms[:]:
                        platform.update(player.rect, dt)
                        platform.draw(screen)

                    player.update(platforms)
                    scroll = 0
                    player.move()
                    player.draw(screen)
                    if player.y < MIDDLE_Y and player.jump_velocity < 0:
                        scroll = MIDDLE_Y - player.y
                        player.y = MIDDLE_Y
                        y = PLATFORM_Y_START - len(platforms) * PLATFORM_Y_SPACING
                        platforms.append(generate_platform(platforms, PLATFORM_X_COORDS, y))
                    score += scroll
                    bg_scroll += scroll
                    if bg_scroll >= SCREEN_HEIGHT:
                        bg_scroll = 0
                        if not first_bg_scrolled:
                            first_bg_scrolled = True
                    for platform in platforms[:]:
                        platform.y += scroll
                        platform.update_rect()
                        if platform.y > SCREEN_HEIGHT:
                            platforms.remove(platform)
                    for enemy in enemies:
                        enemy.rect.y += scroll
                        if enemy.rect.y > SCREEN_HEIGHT:
                            enemies.remove(enemy)

                    enemies.update()
                    enemies.draw(screen)

                    if score >= score_checkpoint:
                        score_checkpoint += 1000
                        generate_enemies()

                    if check_collision(player, enemies):
                        player.stop_jetpack_sound()
                        player.run_sound.stop()
                        game_over = True
                        pygame.mixer.music.stop()
                        game_over_sound.play()
                        if score > best_score:
                            best_score = score
                            # save_best_score(best_score)

                    if player.y > SCREEN_HEIGHT:
                        player.stop_jetpack_sound()
                        player.run_sound.stop()
                        game_over = True
                        pygame.mixer.music.stop()
                        game_over_sound.play()
                        if score > best_score:
                            best_score = score
                            # save_best_score(best_score)

                    draw_score(score)
                    draw_best_score(best_score)
            else:
                player.jetpack_sound.stop()
                draw_game_over()

        pygame.display.update()
        await asyncio.sleep(0)
asyncio.run(main())


