#!/usr/bin/env python3
# ble_relay.py
# Summary: Advertises as a ble device and forwards received commands
# Authors:
# - LeonardoFerrisi


class BLERelay:

    def __init__(self, device_name):
        self.device_name = device_name

    def start_advertising(self):
        # Code to start BLE advertising
        pass

    def stop_advertising(self):
        # Code to stop BLE advertising
        pass

    def handle_received_command(self, command):
        # Code to handle a command received via BLE
        """
        Handle a command received via BLE and forward it to the hardware controller.
        """
        pass

    def relay_command(self, hardware_controller, command):
        # Code to relay a command to the hardware controller
        """
        Relay a command to the given hardware controller.
        """
        pass