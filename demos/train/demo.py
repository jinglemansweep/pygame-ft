import logging
import math
import pygame
import pygame.pkgdata
import random
import os
import sys
import time
from argparse import ArgumentParser
from pygame.locals import QUIT, RESIZABLE, SCALED

from pygameft import FTClient

PANEL_SIZE = (64, 64)
PANEL_LAYOUT = (4, 2)
DISPLAY_LAYOUT = (8, 1)
DISPLAY_SIZE = (PANEL_SIZE[0] * DISPLAY_LAYOUT[0], PANEL_SIZE[1] * DISPLAY_LAYOUT[1])

PYGAME_FPS = 100
PYGAME_SCREEN_DEPTH = 16

_APP_NAME = "pygameft-demo-train"
_APP_DESCRIPTION = "PyGame Flaschen Taschen Demo: Train"
_APP_VERSION = "0.0.1"

parser = ArgumentParser(description=f"{_APP_DESCRIPTION} v{_APP_VERSION}")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-H", "--host", required=True, help="Flaschen-Taschen Host")
parser.add_argument(
    "-p", "--port", type=int, default=1337, help="Flaschen-Taschen Port"
)
parser.add_argument("-l", "--layer", type=int, default=5, help="Flaschen-Taschen Layer")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
logger = logging.getLogger("main")

ft = FTClient(
    host=args.host,
    port=args.port,
    width=PANEL_SIZE[0] * PANEL_LAYOUT[0],
    height=PANEL_SIZE[1] * PANEL_LAYOUT[1],
    tile_width=PANEL_SIZE[0],
    tile_height=PANEL_SIZE[1],
    layer=args.layer,
)

pygame.init()
clock = pygame.time.Clock()
font_large = pygame.font.SysFont("", 64)
font_tiny = pygame.font.SysFont("", 16)
# pygame.event.set_allowed([QUIT])
pygame.display.set_caption(_APP_DESCRIPTION)
screen_flags = RESIZABLE | SCALED
screen = pygame.display.set_mode(DISPLAY_SIZE, screen_flags, PYGAME_SCREEN_DEPTH)

logger.info(f"{_APP_DESCRIPTION} v{_APP_VERSION}")
logger.info(f"Panel Dimensions:     {PANEL_SIZE[0]}px x {PANEL_SIZE[1]}px")
logger.info(f"Display Dimensions:   {DISPLAY_SIZE[0]}px x {DISPLAY_SIZE[1]}px")
logger.info(f"Display Layout:       {DISPLAY_LAYOUT[0]} x {DISPLAY_LAYOUT[1]} (panels)")


def parallelise_surface(surface):
    temp_surface = pygame.Surface(
        (PANEL_SIZE[0] * PANEL_LAYOUT[0], PANEL_SIZE[1] * PANEL_LAYOUT[1]),
    )
    # Blit first 4 panels to top row
    temp_surface.blit(
        surface,
        (0, 0),
        (0, 0, PANEL_SIZE[0] * PANEL_LAYOUT[0], PANEL_SIZE[1] * 1),
    )
    # Blit next 4 panels to next row
    temp_surface.blit(
        surface,
        (0, PANEL_SIZE[1] * 1),
        (
            PANEL_SIZE[0] * PANEL_LAYOUT[0],
            0,
            PANEL_SIZE[0] * PANEL_LAYOUT[0],
            PANEL_SIZE[1],
        ),
    )
    return temp_surface


class Train(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "train.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.x, self.y = float(position[0]), float(position[1])

    def update(self, frame):
        self.x += -1 + (random.random() * 2)
        if frame % 100 == 0:
            self.y -= 1
        if frame % 100 == 10:
            self.y += 1
        self.rect.x, self.rect.y = int(self.x), int(self.y)


def run():
    global screen

    frame = 0
    sprite_group = pygame.sprite.Group()
    px = py = 0

    train = Train((0, 0))
    sprite_group.add(train)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        sprite_group.update(frame)
        sprite_group.draw(screen)
        # render_led_matrix(screen, matrix)
        ft.send_surface(parallelise_surface(screen))
        pygame.display.flip()
        clock.tick(PYGAME_FPS)
        frame += 1


if __name__ == "__main__":
    run()
