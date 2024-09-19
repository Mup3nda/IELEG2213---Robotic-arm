import asyncio
from bleak import BleakScanner

async def find_connected_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.rssi != 0:  # Typically, connected devices have an RSSI (signal strength) value
            print(f"Device: {device.name}, Address: {device.address}, RSSI: {device.rssi}")

loop = asyncio.get_event_loop()
loop.run_until_complete(find_connected_devices())
