import pygame
from core import exit_if_user_pressed_quit

pygame.init()
screen = pygame.display.set_mode((400, 300))

clock = pygame.time.Clock()
frames_per_second = 15

while True:

    exit_if_user_pressed_quit()

    # Fill the screen with white
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 255, 0), (200, 150), 50)  # Draw a green circle

    # Update the display
    pygame.display.flip()

    clock.tick(frames_per_second)
