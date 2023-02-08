# PyGame Bridge for Flaschen Taschen

An attempt to provide a way of broadcasting PyGame controlled scenes (or even games) to a HUB75 RGB Matrix using [flaschen-taschen](https://github.com/hzeller/flaschen-taschen) and the excellent [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) libraries.

## Introduction

This project aims to provide a simple bridge between [PyGame](https://www.pygame.org) using [Flaschen Taschen](https://github.com/hzeller/flaschen-taschen) which provides a UDP interface for "pushing pixels" (sending images, animations, text, video etc.) to HUB75 RGB Matrix panels.

It is possible to send a 2D array of pixel colours, but due to the limitation of UDP packet size (64KiB), pushing pixel updates for regions larger than 64x64 will likely fail.

This bridge provides a simple function that can be dropped in any PyGame loop that accepts the current display's [PyGame Surface](https://www.pygame.org/docs/ref/surface.html). The function then tiles the surface into small enough UDP packets and sends them to the Flaschen Taschen server.

This is a simple example of the bridge in action:

    from pygameft import FTClient
    
    DISPLAY_SIZE = (256, 128)
    TILE_SIZE = (64, 64)
    ft = FTClient(
        "ftserver.local", 
        width=DISPLAY_SIZE[0], height=DISPLAY_SIZE[1], 
        tile_width=TILE_SIZE[0], tile_height=TILE_SIZE[1]
    )

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    while True:
        # game logic and blitting goes here
        ft.send_surface(screen)
        pygame.display.flip()
        clock.tick()

The following diagram illustrates a 4x2 panel arrangement of 64x64 RGB matrix panels. The single 256x128 surface is divided into eight 64x64 tiles. Each tile is then sent to the Flaschen Taschen server via UDP:
    
                                                          dx: 256
    +--------------+--------------+--------------+--------------+ 
    | (0,0)        | (64,0)       | (128,0)      | (192,0)      |
    |              |              |              |              |
    |              |              |              |              |
    |              |              |              |              |
    |      (64,64) |              |              |              |
    +--------------+--------------+--------------+--------------+ 
    | (0,64)       | (64,64)      | (128,64)     | (192,64)     |
    |              |              |              |              |
    |              |              |              |              |
    |              |              |              |              |
    |      (64,64) |              |              |              |
    +--------------+--------------+--------------+--------------+ dy: 128
    

## Installation

Fetch the required `flaschen-taschen` and `rpi-rgb-led-matrix` repo submodules:

    git submodule update --init --recursive

Create a virtual environment, and install dependencies:

    python -m venv ./venv
    source ./venv/bin/activate
    poetry install # or 'pip install .'

Build the `flaschen-taschen` server component:

    cd ./lib/flaschen-taschen/server
    make FT_BACKEND=rgb-matrix # or "terminal"

Optionally, build the Python bindings for `rpi-rgb-led-matrix`:

    cd ./lib/flaschen-taschen/server/rgb-matrix
    make build-python

Install the example `systemd` service definition:

    cp ./etc/systemd/system/ft-server.service /etc/systemd/system/
    systemctl daemon-reload

Configure the project by either creating a `.env` file (see [`.env.example`](./.env.example) for details):

    cp ./.env.example ./.env
    ${EDITOR} ./.env

Alternatively, copy and modify the provided `systemd` defaults environment file:

    cp ./etc/default/ft-server /etc/default/

Start and optionally enable the server on boot:

    systemctl start ft-server
    systemctl enable ft-server

