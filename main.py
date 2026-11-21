from pathlib import Path
import random

import pygame


pygame.init()

WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 96
PLAYER_SPEED = 6
METEOR_WIDTH, METEOR_HEIGHT = 64, 96
METEOR_SPEED = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the meteor")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

assets_dir = Path(__file__).resolve().parent / "imgs"
player = pygame.image.load(str(assets_dir / "player.png")).convert_alpha()
player = pygame.transform.scale(player, (PLAYER_SIZE, PLAYER_SIZE))

meteor = pygame.image.load(str(assets_dir / "meteor.png")).convert_alpha()
meteor = pygame.transform.scale(meteor, (METEOR_WIDTH, METEOR_HEIGHT))

player_rect = player.get_rect(midbottom=(WIDTH // 2, HEIGHT - 16))
meteor_rect = meteor.get_rect(midtop=(random.randrange(WIDTH - METEOR_WIDTH + 1), -METEOR_HEIGHT))
score = 0
game_over = False
running = True
vel_incicial = 5
intervalo = 5
aumento = 3
vel_max = 50
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
            player_rect.midbottom = (WIDTH // 2, HEIGHT - 16)
            meteor_rect.midtop = (random.randrange(WIDTH - METEOR_WIDTH + 1), -METEOR_HEIGHT)
            score = 0
            game_over = False
    nivel = score//intervalo
    meteor_vel_y = min(
        vel_incicial + nivel  * aumento,
        vel_max)    

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += PLAYER_SPEED
        player_rect.clamp_ip(window.get_rect())

        meteor_rect.y += meteor_vel_y
        if meteor_rect.top > HEIGHT:
            meteor_rect.midtop = (random.randrange(WIDTH - METEOR_WIDTH + 1), -METEOR_HEIGHT)
            score += 1

        if player_rect.colliderect(meteor_rect):
            game_over = True

    window.fill((15, 18, 32))
    window.blit(player, player_rect)
    window.blit(meteor, meteor_rect)

    score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
    window.blit(score_text, (16, 16))

    if game_over:
        title = font.render("Game over", True, (255, 220, 220))
        restart = small_font.render("Press R to restart or close the window to quit", True, (255, 255, 255))
        window.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        window.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()