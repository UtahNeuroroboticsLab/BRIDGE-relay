import logging
import json
import datetime
import math # Import math for sine wave

from bluezero import adapter
from bluezero import peripheral
from bluezero import async_tools

# --- Configuration ---
# Custom UUIDs (Randomly generated for this example)
SRV_UUID = '5153BCD7-6CF5-465B-BEA5-E7B1F43B00D7' 
RX_UUID  = 'B5A513B3-3027-41A7-B015-5BD69A75ED53' 
TX_UUID  = 'C193480F-7BBC-41A9-BB07-15131D0D2D39' 

DEVICE_NAME = 'Pi_JSON_Server'

# The base JSON structure
DATA_TO_SEND = {
    "timestamp": "", # Placeholder
    "sensor": "temperature",
    "value": 0.0, # Placeholder
    "unit": "C",
    "status": "active",
    "meta": "Sine wave data stream."
}

class BLESender:
    def __init__(self):
        self.app = peripheral.Peripheral(adapter.list_adapters()[0], 
                                         local_name=DEVICE_NAME)
        
        # Add Service
        self.app.add_service(srv_id=1, uuid=SRV_UUID, primary=True)

        # Add RX Characteristic (Write)
        self.app.add_characteristic(srv_id=1, chr_id=1, uuid=RX_UUID,
                                    value=[], notifying=False,
                                    flags=['write', 'write-without-response'],
                                    write_callback=self.on_rx_write,
                                    read_callback=None,
                                    notify_callback=None)

        # Add TX Characteristic (Notify)
        self.app.add_characteristic(srv_id=1, chr_id=2, uuid=TX_UUID,
                                    value=[], notifying=False,
                                    flags=['notify'],
                                    write_callback=None,
                                    read_callback=None,
                                    notify_callback=self.on_tx_subscribe)

        # State tracking
        self.streaming = False
        self.sine_x = 0.0 # Tracks the position in the sine wave

    def on_rx_write(self, value, options):
        """Called when the client writes data to the RX characteristic."""
        try:
            decoded = bytes(value).decode('utf-8')
            print(f"Received data: {decoded}")
        except Exception as e:
            print(f"Received binary data: {bytes(value)}")

    def on_tx_subscribe(self, notifying, characteristic):
        """
        Triggered when client Subscribes (True) or Unsubscribes (False).
        """
        if notifying:
            print("Client subscribed. Starting continuous sine wave stream...")
            self.streaming = True
            
            # Start the loop. 0.5s is the delay between updates.
            async_tools.add_timer_seconds(0.5, self.send_json_chunks, characteristic)
            return True 
        else:
            print("Client unsubscribed. Stopping stream.")
            self.streaming = False
            return False

    def send_json_chunks(self, characteristic):
        """
        Updates the JSON with a new sine value, chunks it, and sends it.
        Returns True to repeat (loop), False to stop.
        """
        # 1. Safety Check: Stop if client disconnected
        if not self.streaming:
            return False

        # 2. Update Data (Sine Wave Math)
        # Formula: Amplitude * sin(x) + Offset
        # Creates a wave oscillating between 15 and 35
        self.sine_x += 0.2
        new_value = 25.0 + (10.0 * math.sin(self.sine_x))
        
        DATA_TO_SEND["value"] = round(new_value, 2)
        DATA_TO_SEND["timestamp"] = datetime.datetime.now().isoformat()

        # 3. Prepare JSON (Adding \n delimiter is best practice for streams)
        json_str = json.dumps(DATA_TO_SEND) + "\n"
        data_bytes = json_str.encode('utf-8')
        
        # 4. Chunk and Send
        CHUNK_SIZE = 1
        
        # Note: We silence the print here to avoid spamming the console 
        # print(f"Sending value: {new_value}") 
        
        for i in range(0, len(data_bytes), CHUNK_SIZE):
            chunk = data_bytes[i:i + CHUNK_SIZE]
            try:
                characteristic.set_value(chunk)
            except Exception as e:
                # If sending fails (e.g., immediate disconnect), stop the loop
                print(f"Send failed: {e}")
                self.streaming = False
                return False
            
        # 5. Return True to keep this function running repeatedly
        return True 

    def run(self):
        print(f"Starting BLE Server: {DEVICE_NAME}")
        # The publish loop blocks here until Ctrl-C
        self.app.publish()

if __name__ == '__main__':
    sender = BLESender()
    sender.run()