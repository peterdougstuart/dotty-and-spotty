import pygame
import sys
import random
from pygame.locals import *
from os.path import join

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Clock for controlling frame rate
clock = pygame.time.Clock()
fps = 15


# Load Spritesheets
def load_spritesheet(filename, frame_count, frame_width, frame_height, flip=False):
    spritesheet = pygame.image.load(filename).convert_alpha()
    frames = []
    flipped_frames = []
    for i in range(frame_count):
        frame = spritesheet.subsurface(
            pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        )

        frame = pygame.transform.scale(
            frame, (frame_width * 2, frame_height * 2)
        )  # Double the size

        frames.append(frame)
        if flip:
            flipped_frame = pygame.transform.flip(
                frame, True, False
            )  # Flip horizontally
            flipped_frames.append(flipped_frame)
    return frames, flipped_frames if flip else frames


# Dictionary of animations
animations = {}
original_walk, flipped_walk = load_spritesheet(
    join("images", "cat1", "cat01_walk_strip8.png"),
    8,
    40,
    40,
    flip=True,
)
animations["walk-right"] = original_walk
animations["walk-left"] = flipped_walk

original_run, flipped_run = load_spritesheet(
    join("images", "cat1", "cat01_run_strip4.png"),
    4,
    40,
    40,
    flip=True,
)

animations["run-right"] = original_run
animations["run-left"] = flipped_run

# Idle and sneak only have one direction in this setup
animations["idle"], _ = load_spritesheet(
    join("images", "cat1", "cat01_idle_strip8.png"),
    8,
    40,
    40,
)
animations["sneak"], _ = load_spritesheet(
    join("images", "cat1", "cat01_sneak_strip8.png"),
    8,
    40,
    40,
)

# Movement parameters
movement_data = {
    "walk-right": (2, 0),
    "walk-left": (-2, 0),
    "run-right": (5, 0),
    "run-left": (-5, 0),
    "idle": (0, 0),
    "sneak": (1, 0),
}

# Character attributes
position = [screen_width // 2, screen_height // 2]
current_action = "idle"
frame_index = 0
action_timer = 0
action_duration = random.randint(60, 180)  # Frames until action change

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Update the animation frame
    frame_index += 1
    if frame_index >= len(animations[current_action]):
        frame_index = 0

    # Move the character
    position[0] += movement_data[current_action][0]
    position[1] += movement_data[current_action][1]

    # Ensure the character stays within bounds
    position[0] = max(0, min(screen_width, position[0]))

    # Randomly change actions
    action_timer += 1
    if action_timer > action_duration:
        action_timer = 0
        action_duration = random.randint(60, 180)
        current_action = random.choice(list(animations.keys()))

    # Clear screen
    screen.fill((0, 0, 0))
    # Draw the current frame
    screen.blit(animations[current_action][frame_index], position)

    # Update display
    pygame.display.flip()
    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
