import pygameft

import logging
import math
import os
import pygame
import pygame.pkgdata
import random
import sys
import time
import uuid
from argparse import ArgumentParser
from pygame.locals import QUIT, RESIZABLE, SCALED


sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

PANEL_SIZE = (64, 64)
DISPLAY_LAYOUT = (8, 1)
DISPLAY_SIZE = (PANEL_SIZE[0] * DISPLAY_LAYOUT[0], PANEL_SIZE[1] * DISPLAY_LAYOUT[1])

PYGAME_FPS = 120

_APP_NAME = "pygameft-demo"
_APP_DESCRIPTION = "PyGame Flaschen Taschen Demo"
_APP_VERSION = "0.0.1"

parser = ArgumentParser(description=f"{_APP_DESCRIPTION} v{_APP_VERSION}")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

pygame.init()
clock = pygame.time.Clock()
font_large = pygame.font.SysFont("", 96)
font_tiny = pygame.font.SysFont("", 16)
# pygame.event.set_allowed([QUIT])
pygame.display.set_caption(_APP_DESCRIPTION)
screen_flags = RESIZABLE | SCALED
screen = pygame.display.set_mode(DISPLAY_SIZE, screen_flags, 16)

logger.info(f"RGB Matrix")
logger.info(f"Panel Dimensions:     {PANEL_SIZE[0]}px x {PANEL_SIZE[1]}px")
logger.info(f"Display Dimensions:   {DISPLAY_SIZE[0]}px x {DISPLAY_SIZE[1]}px")
logger.info(f"Display Layout:       {DISPLAY_LAYOUT[0]} x {DISPLAY_LAYOUT[1]} (panels)")


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, index, width=64, height=64, color=None):
        super().__init__()
        self.width = width
        self.height = height
        self.index = index
        self.color = color or random_color()
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

    def update(self, frame):
        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.rect(
            self.image,
            self.color,
            pygame.Rect(0, 0, self.width, self.height),
        )
        step = frame * 0.1
        step %= 2 * math.pi
        frame_sine = -1 * math.sin(step) * 1
        text_dimensions = font_tiny.render(
            f"{self.width}x{self.height}", False, (255, 255, 255)
        )
        self.image.blit(text_dimensions, (2, 2))
        text_index_offset = (10, 1)
        text_index_shadow = font_large.render(str(self.index), True, (0, 0, 0))
        text_index = font_large.render(str(self.index), True, (255, 255, 255))
        scale = 0.9 + (frame_sine * 0.1)
        rotation = frame_sine * 5
        self.image.blit(
            pygame.transform.rotozoom(text_index_shadow, rotation, scale),
            (text_index_offset[0] + 2, text_index_offset[1] + 2),
        )
        self.image.blit(
            pygame.transform.rotozoom(text_index, rotation, scale),
            (text_index_offset[0], text_index_offset[1]),
        )

    def _build_label(self, index):
        return f"{index}"


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def run():

    frame = 0

    px = 0
    py = 0

    sprites_panels = pygame.sprite.Group()

    for pi in range(0, DISPLAY_LAYOUT[0] * DISPLAY_LAYOUT[1]):
        for pc in range(0, DISPLAY_LAYOUT[0]):
            sprites_panels.add(
                Square(px, py, index=pc, width=PANEL_SIZE[0], height=PANEL_SIZE[1])
            )
            px += PANEL_SIZE[0]
            if px >= PANEL_SIZE[0] * DISPLAY_LAYOUT[0]:
                px = 0
                py += PANEL_SIZE[1]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        sprites_panels.update(frame)
        sprites_panels.draw(screen)
        # render_led_matrix(screen, matrix)
        pygame.display.flip()
        clock.tick(PYGAME_FPS)
        frame += 1


if __name__ == "__main__":
    run()
