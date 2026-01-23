# dev/bluezero_testing

Run `main.py` to start a basic server using bluezero and bluez in a linux environment.

Connecting to this using BRIDGE should allow for effective transmission of data over BLE.

## Some pre-reqs

(Tested on Raspberry Pi Zero 2W)

Firstly, make sure you have a virtual environemnt created:

```bash
python -m venv .venv
```

Then activate using
```bash
source .venv\bin\activate
```

Then, you need to have an up-to-date linux system.

run the following commands

```bash
sudo apt update
sudo apt install build-essential libdbus-1-dev libglib2.0-dev libgirepository1.0-dev libcairo2-dev pkg-config python3-dev
```

(optional) upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

Finally, install bluezero:
```bash
pip install bluezero
```