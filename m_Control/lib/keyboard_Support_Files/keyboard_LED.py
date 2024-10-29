import asyncio
from bleak import BleakClient
import keyboard

# BLE address of the ESP32
ADDRESS = "d4:f9:8d:03:ee:6a"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-abc123456789"

# Mapping of keys to commands
key_to_command = {
    "pil venstre": "D2_toggle",
    "pil opp": "D3_toggle",
    "pil ned": "D4_toggle",
    "pil høyre": "D5_toggle"
}

async def send_command(client, command):
    await client.write_gatt_char(CHARACTERISTIC_UUID, command.encode())

async def main():
    attempt = 1
    client = BleakClient(ADDRESS)
    while not client.is_connected:
        print(f"Trying to connect to ESP32, attempt: {attempt}")
        try:
            await client.connect()
        except Exception as e:
            print(f"Connection attempt {attempt} failed: {e}")
        attempt += 1
        await asyncio.sleep(1)
    
    print("Connected to ESP32")

    def on_key_event(event):
        key = event.name
        if key in key_to_command:
            command = key_to_command[key]
            print(f"Pressed key: {key}, sending command: {command}")
            asyncio.run(send_command(client, command))
        else:
            print(f"Pressed key: {key}, sent nothing")

    # Set up the listener for key press events
    keyboard.on_press(on_key_event)

    # Keep the script running and listening for events
    keyboard.wait()

# Run the main function
asyncio.run(main())