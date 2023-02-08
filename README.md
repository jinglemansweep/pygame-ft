# PyGame Bridge for Flaschen Taschen

An attempt to provide a way of broadcasting PyGame controlled scenes (or even games) to a HUB75 RGB Matrix using [flaschen-taschen](https://github.com/hzeller/flaschen-taschen) and the excellent [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) libraries.

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

