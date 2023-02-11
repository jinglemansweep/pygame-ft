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
        logger.info(
            f"{_NAME}: host={host} port={port} width={width} height={height} layer={layer} transparent={transparent} tile_width={tile_width} tile_height={tile_height}"
        )
        self.client = Flaschen(
            self.host, self.port, self.width, self.height, self.layer, self.transparent
        )

    def send_surface(self, surface, wrap=True, layer=None):
        layer = layer or self.layer
        if wrap is True:
            surface = self.wrap_surface(surface)
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

    def wrap_surface(self, surface):
        temp_surface = pygame.Surface((self.width, self.height))
        x_tiles = self.width // self.tile_width
        y_tiles = self.height // self.tile_height

        row = 0
        while row <= y_tiles:
            y = row * self.tile_height
            x = self.tile_width * (x_tiles * row)
            temp_surface.blit(
                surface,
                (0, y),
                (x, 0, self.tile_width * x_tiles, self.tile_height * 1),
            )
            row += 1
        return temp_surface
