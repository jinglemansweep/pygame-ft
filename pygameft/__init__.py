import logging
import numpy as np
import pygame
from pygameft.flaschen import Flaschen

_NAME = "ftclient"

logger = logging.getLogger(_NAME)


class FTClient:
    def __init__(
        self,
        host="localhost",
        port=1337,
        position=(0, 0),
        size=(64, 64),
        layer=5,
        transparent=True,
        tile_size=(64, 64),
    ):
        self.host = host
        self.port = port
        self.position = position
        self.size = size
        self.layer = layer
        self.transparent = transparent
        self.tile_size = tile_size
        logger.info(
            f"{_NAME}: host={host} port={port} position={position} size={size} layer={layer} transparent={transparent} tile_size={tile_size}"
        )
        self.client = Flaschen(
            self.host,
            self.port,
            self.size[0],
            self.size[1],
            self.layer,
            self.transparent,
        )

    def send_surface(self, surface, wrap=True, layer=None):
        layer = layer or self.layer
        if wrap is True:
            surface = self.wrap_surface(surface)
        pixel_array = pygame.surfarray.pixels3d(surface)
        pixel_array = np.rot90(np.fliplr(pixel_array), 1)
        ti = tx = ty = 0
        for ti in range(
            0, (self.size[0] // self.tile_size[0]) * (self.size[1] // self.tile_size[1])
        ):
            if tx >= self.size[0]:
                tx = 0
                ty += self.tile_size[1]
            slice = pixel_array[
                ty : ty + self.tile_size[1], tx : tx + self.tile_size[0]
            ]
            self.client.send_array(
                slice, (self.position[0] + tx, self.position[1] + ty, layer)
            )
            tx += self.tile_size[0]

    def wrap_surface(self, surface):
        temp_surface = pygame.Surface(self.size)
        x_tiles = self.size[0] // self.tile_size[0]
        y_tiles = self.size[1] // self.tile_size[1]

        row = 0
        while row <= y_tiles:
            y = row * self.tile_size[1]
            x = self.tile_size[0] * (x_tiles * row)
            temp_surface.blit(
                surface,
                (0, y),
                (x, 0, self.tile_size[0] * x_tiles, self.tile_size[1] * 1),
            )
            row += 1
        return temp_surface
