#!/usr/bin/env python3
import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
RX_UUID      = "12345678-1234-5678-1234-56789abcdef1"  # Write to this
TX_UUID      = "12345678-1234-5678-1234-56789abcdef2"  # Read from this


def on_response(sender, data):
    """Print responses from RPi"""
    msg = data.decode().strip()
    if msg:
        print(f"\nRPi: {msg}")


def validate_input(msg: str) -> bool:
    """Check that input is exactly 6 whole numbers separated by spaces."""
    parts = msg.strip().split()
    if len(parts) != 6:
        return False
    try:
        [int(p) for p in parts]
        return True
    except ValueError:
        return False


async def main():
    # Find RPi
    print("Scanning...")
    devices = await BleakScanner.discover(timeout=15.0)
    address = None
    for d in devices:
        if d.name == "raspberrypi":
            address = d.address
            break

    if not address:
        print("raspberrypi not found!")
        return

    # Connect
    print(f"Connecting to {address}...")
    async with BleakClient(address) as client:

        # ✅ Force service discovery before any characteristic operations
        await client.get_services()

        # Subscribe to TX characteristic for notifications
        await client.start_notify(TX_UUID, on_response)

        print("Connected! Enter 6 numbers separated by spaces (e.g. 0 0 200 0 0 100)")
        print("Type 'bye' to quit.\n")

        loop = asyncio.get_event_loop()
        while True:
            msg = await loop.run_in_executor(None, input, "You: ")
            msg = msg.strip()

            if msg == "bye":
                await client.write_gatt_char(RX_UUID, msg.encode())
                break

            if not msg:
                continue

            if not validate_input(msg):
                print("Invalid input. Please enter exactly 6 whole numbers, e.g.: 0 0 200 0 0 100")
                continue

            await client.write_gatt_char(RX_UUID, msg.encode())
            await asyncio.sleep(0.1)


asyncio.run(main())