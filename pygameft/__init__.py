import logging
import numpy as np
import pygame
from pygameft.flaschen import Flaschen

logger = logging.getLogger("ftclient")


class FTClient:
    def __init__(
        self,
        host="localhost",
        port=1337,
        width=64,
        height=64,
        layer=5,
        transparent=True,
        tile_width=64,
        tile_height=64,
    ):
        self.host = host
        self.port = port
        self.width = width
        self.height = height
        self.layer = layer
        self.transparent = transparent
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.client = Flaschen(
            self.host, self.port, self.width, self.height, self.layer, self.transparent
        )

    def send_surface(self, surface, layer=None):
        layer = layer or self.layer
        pixel_array = pygame.surfarray.pixels3d(surface)
        pixel_array = np.rot90(np.fliplr(pixel_array), 1)
        ti = tx = ty = 0
        for ti in range(
            0, (self.width // self.tile_width) * (self.height // self.tile_height)
        ):
            if tx >= self.width:
                tx = 0
                ty += self.tile_height

            slice = pixel_array[ty : ty + self.tile_height, tx : tx + self.tile_width]
            self.client.send_array(slice, (tx, ty, layer))

            tx += self.tile_width
