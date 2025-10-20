#!/usr/bin/env python3
# control_hardware.py
# Summary: Code for controlling hardware components of the BRIDGE-relay system
# Authors:
# - LeonardoFerrisi

class HardwareController:

    def __init__(self, port, baudrate):

        self.commands = {
            "ECHO": "echo" # Causes the hardware to respond with an acknowledgment
        }
        pass

    def initialize_hardware(self):
        # Code to initialize hardware components
        pass
    
    def load_commands(self, settings_path):
        """
        Loads commands from a settings json file and adds them
        to self.commands
        """
        pass

    def send_command(self, command):
        # Code to send a command to the hardware
        """
        Send a command (string key) to the hardware component.
        Only works if command is in self.commands.
        """
        pass

    def control_component(self, component_id, action):
        # Code to control a specific hardware component
        pass

