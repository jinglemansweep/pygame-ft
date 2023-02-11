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
PANEL_LAYOUT = (4, 3)
DISPLAY_LAYOUT = (12, 1)
DISPLAY_SIZE = (PANEL_SIZE[0] * DISPLAY_LAYOUT[0], PANEL_SIZE[1] * DISPLAY_LAYOUT[1])

PYGAME_FPS = 50
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
    tile_width=PANEL_SIZE[0] * 4,
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


class Train(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "train.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.x, self.y = float(position[0]), float(position[1])
        self.direction = 1
        self.velocity = [0.0, 0.0]
        self.accel = [0.0, 0.0]
        self.accel_amount = 1.005
        self.moving = False
        self.velocity_max = [128.0, 5.0]
        self.friction = 0.995

    def update(self, frame):
        if frame % 1000 == 0 and int(self.velocity[0]) == 0:
            self.direction = random.choice([-1, 1])
            logger.info(f"moving direction={self.direction}")
            self.accel[0] = 0.001
            self.moving = True

        if self.moving:
            self.accel[0] *= self.accel_amount
        else:
            self.accel[0] = 0

        self.velocity[0] += self.accel[0]
        if self.velocity[0] > self.velocity_max[0]:
            logger.info(f"stopping velocity={self.velocity[0]}")
            self.velocity[0] = self.velocity_max[0]
            self.moving = False

        self.x += self.velocity[0] * self.direction
        self.velocity[0] *= self.friction
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
        if train.x > DISPLAY_SIZE[0]:
            train.x = 0 - train.rect.width
        if train.x < 0 - train.rect.width:
            train.x = DISPLAY_SIZE[0]
        sprite_group.update(frame)
        sprite_group.draw(screen)
        ft.send_surface(
            screen,
        )
        pygame.display.flip()
        clock.tick(PYGAME_FPS)
        frame += 1


if __name__ == "__main__":
    run()
