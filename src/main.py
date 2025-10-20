#!/usr/bin/env python3
# main.py
# Summary: Entry point for the BRIDGE-relay application
# Authors:
# - LeonardoFerrisi


from control_hardware import HardwareController
from ble_relay import BLERelay
import logging


def main():

    # Start BLE Relay

    # Start Hardware Controller

    # In a loop, if BLE Relay recieves a command, forward it to Hardware Controller

    logging.basicConfig(level=logging.INFO)
    logging.info("BRIDGE-relay application started.")
    ble_relay = BLERelay(device_name="BRIDGE-relay-device")
    ble_relay.start_advertising()
    hardware_controller = HardwareController(port="/dev/ttyUSB0", baudrate=9600)
    hardware_controller.initialize_hardware()

    try:
        while True:
            # Placeholder for receiving command via BLE
            received_command = None  # Replace with actual BLE command reception logic

            if received_command:
                logging.info(f"Received command via BLE: {received_command}")
                ble_relay.relay_command(hardware_controller, received_command)
                logging.info(f"Relayed command to hardware: {received_command}")
    except KeyboardInterrupt:
        logging.info("Shutting down BRIDGE-relay application.")
    ble_relay.stop_advertising()

if __name__ == "__main__":
    main()
