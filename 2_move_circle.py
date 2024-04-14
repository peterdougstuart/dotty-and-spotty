import pygame
from core import exit_if_user_pressed_quit

pygame.init()
screen = pygame.display.set_mode((400, 300))

clock = pygame.time.Clock()
frames_per_second = 15
x, y = 175, 125

while True:

    exit_if_user_pressed_quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 1
    if keys[pygame.K_RIGHT]:
        x += 1
    if keys[pygame.K_UP]:
        y -= 1
    if keys[pygame.K_DOWN]:
        y += 1

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), (x, y, 50, 50))

    # Update the display
    pygame.display.flip()

    clock.tick(frames_per_second)
