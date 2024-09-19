import asyncio
from bleak import BleakClient

# ESP32 address and UUIDs from your code
esp32_address = "d4:f9:8d:03:ee:6a"
service_uuid = "12345678-1234-1234-1234-123456789abc"
characteristic_uuid = "87654321-4321-4321-4321-abc123456789"

client = None

async def connect_to_esp32():
    global client
    client = BleakClient(esp32_address)
    await client.connect()
    print(f"Connected to ESP32: {esp32_address}")

async def send_command_to_esp32(command):
    if client and client.is_connected:
        await client.write_gatt_char(characteristic_uuid, command.encode())
        print(f"Sent command: {command}")
    else:
        print("Client not connected")

async def disconnect_from_esp32():
    global client
    if client:
        await client.disconnect()
        print(f"Disconnected from ESP32: {esp32_address}")