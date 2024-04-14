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
font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the font size


# Load cursor images or set system cursor for hand
hand_cursor = pygame.cursors.compile(
    pygame.cursors.sizer_x_strings
)  # This is just a placeholder, use the appropriate hand cursor
arrow_cursor = pygame.mouse.get_cursor()  # Save the default cursor


# Function to change cursor to hand
def set_hand_cursor():
    pygame.mouse.set_cursor(
        *pygame.cursors.arrow
    )  # Placeholder: replace with the actual hand cursor setup


# Function to reset cursor to default
def set_arrow_cursor():
    pygame.mouse.set_cursor(*arrow_cursor)


class Action:
    def __init__(self, name, path, flipx, dx, dy, frames, max_repeats=10):
        self.name = name
        self.path = path
        self.flipx = flipx
        self.dx = dx
        self.dy = dy
        self.frames = frames
        self.max_repeats = max_repeats


class Cat:
    def __init__(self, actions):

        self.frame_width = 40
        self.frame_height = 40

        self.actions = actions
        self.animations = self.load_animations(actions)

        self.current_action = random.choice(actions)
        self.frame_index = 0

        self.position = [
            random.randint(0, screen_width),
            random.randint(0, screen_height),
        ]

        self.action_repeat_count = 1
        self.action_repeats = random.randint(1, self.current_action.max_repeats)

        self.info = [
            ("This kitty likes its tummy tickled", "cat_image1.png"),
            ("This kitty loves salmon", "cat_image2.png"),
            ("This kitty loves a backstroke", "cat_image3.png"),
            ("This kitty loves to play with yarn", "cat_image4.png"),
            ("This kitty enjoys napping in the sun", "cat_image5.png"),
        ]

        self.rect = pygame.Rect(
            self.position[0],
            self.position[1],
            self.frame_width,
            self.frame_height,
        )
        # self.image = pygame.image.load(image).convert_alpha()

    def get_info(self):
        return random.choice(self.info)[0], None

    def load_animations(self, actions):

        animations = {}

        for action in actions:

            frames = []
            spritesheet = pygame.image.load(action.path).convert_alpha()

            for i in range(action.frames):
                frame = spritesheet.subsurface(
                    pygame.Rect(
                        i * self.frame_width, 0, self.frame_width, self.frame_height
                    )
                )

                frame = pygame.transform.scale(
                    frame, (self.frame_width * 2, self.frame_height * 2)
                )  # Double the size

                if action.flipx:
                    frame = pygame.transform.flip(frame, True, False)

                frames.append(frame)

            animations[action.name] = frames

        return animations

    def update(self):

        self.position[0] += self.current_action.dx
        self.position[1] += self.current_action.dy

        if self.position[0] > screen_width:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = screen_width

        if self.position[1] > screen_height:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = screen_height

        self.rect.topleft = (
            self.position[0] + self.frame_width * 0.5,
            self.position[1] + self.frame_height,
        )

        self.frame_index += 1

        if self.frame_index > len(self.animations[self.current_action.name]) - 1:
            self.frame_index = 0
            self.action_repeat_count += 1

        if self.action_repeat_count > self.action_repeats:

            next_action = random.choice(self.actions)

            while next_action.name == self.current_action.name:
                next_action = random.choice(self.actions)

            self.current_action = next_action

            self.action_repeat_count = 1
            self.action_repeats = random.randint(1, self.current_action.max_repeats)
            self.frame_index = 0

    def draw(self, surface):
        frame = self.animations[self.current_action.name][self.frame_index]
        surface.blit(frame, self.position)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)


# Load multiple cats

cats = []

for i in range(1, 6):  # For 5 different cat spritesheets

    movements = [
        Action(
            name="idle",
            path=join("images", f"cat{i}", f"cat0{i}_idle_strip8.png"),
            flipx=False,
            frames=8,
            dx=0,
            dy=0,
        ),
        Action(
            name="walk-right",
            path=join("images", f"cat{i}", f"cat0{i}_walk_strip8.png"),
            flipx=False,
            frames=8,
            dx=2,
            dy=0,
        ),
        Action(
            name="walk-left",
            path=join("images", f"cat{i}", f"cat0{i}_walk_strip8.png"),
            flipx=True,
            frames=8,
            dx=-2,
            dy=0,
        ),
        Action(
            name="run-right",
            path=join("images", f"cat{i}", f"cat0{i}_run_strip4.png"),
            frames=4,
            flipx=False,
            dx=5,
            dy=0,
        ),
        Action(
            name="run-left",
            path=join("images", f"cat{i}", f"cat0{i}_run_strip4.png"),
            frames=4,
            flipx=True,
            dx=-5,
            dy=0,
        ),
        Action(
            name="sneak-right",
            path=join("images", f"cat{i}", f"cat0{i}_sneak_strip8.png"),
            frames=8,
            flipx=False,
            dx=1,
            dy=0,
        ),
        Action(
            name="sneak-left",
            path=join("images", f"cat{i}", f"cat0{i}_sneak_strip8.png"),
            frames=8,
            flipx=True,
            dx=-1,
            dy=0,
        ),
        Action(
            name="fall-right",
            path=join("images", f"cat{i}", f"cat0{i}_fall_strip3.png"),
            frames=3,
            flipx=False,
            dx=1,
            dy=2,
            max_repeats=1,
        ),
        Action(
            name="fall-left",
            path=join("images", f"cat{i}", f"cat0{i}_fall_strip3.png"),
            frames=3,
            flipx=True,
            dx=-1,
            dy=2,
            max_repeats=1,
        ),
        Action(
            name="jump-right",
            path=join("images", f"cat{i}", f"cat0{i}_jump_strip4.png"),
            frames=4,
            flipx=False,
            dx=1,
            dy=-4,
            max_repeats=1,
        ),
        Action(
            name="jump-left",
            path=join("images", f"cat{i}", f"cat0{i}_jump_strip4.png"),
            frames=4,
            flipx=True,
            dx=-1,
            dy=-4,
            max_repeats=1,
        ),
    ]

    for _ in range(6):  # Create 6 instances of each cat type
        cats.append(Cat(movements))

# Information display area
info_surface = pygame.Surface((screen_width, 40))
info_surface.fill((200, 200, 200))  # grey background for the info box
info_surface_position = (0, 0)  # Position of the info box on the main screen

selected_info = None
selected_image = None
selected_timer = 0  # Timer for how long to display the message

running = True

while running:

    mouse_over_cat = False

    if selected_info is not None and (pygame.time.get_ticks() - selected_timer) > 3000:
        selected_info = None
        selected_image = None

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.locals.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for cat in cats:
                if cat.rect.collidepoint(mouse_pos):
                    selected_info, selected_image = cat.get_info()
                    selected_timer = pygame.time.get_ticks()
                    break

    # Update all cats
    for cat in cats:
        cat.update()
        if cat.rect.collidepoint(pygame.mouse.get_pos()):
            mouse_over_cat = True

    # Set cursor based on mouse position
    if mouse_over_cat:
        set_hand_cursor()
    else:
        set_arrow_cursor()

    # Clear screen with white background
    screen.fill((255, 255, 255))  # RGB color for white

    # Draw all cats
    for cat in cats:
        cat.draw(screen)

    info_surface.fill((200, 200, 200))

    # Display selected cat info
    if selected_info:

        text_surface = font.render(
            selected_info,
            True,
            (0, 0, 0),
        )

        if selected_image is not None:
            info_surface.blit(selected_image, (10, 10))

        info_surface.blit(text_surface, (80, 10))
        screen.blit(info_surface, info_surface_position)

    # Update display
    pygame.display.flip()
    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()
