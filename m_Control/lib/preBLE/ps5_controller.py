import asyncio
from inputs import get_gamepad
from bleak import BleakClient
from m_Control.lib.preBLE.esp32_ble_control import send_command_to_esp32

# Replace with the actual address of your PS5 controller
ps5_controller_address = "7C:66:EF:83:DC:22"

async def connect_ps5_controller():
    async with BleakClient(ps5_controller_address) as client:
        print(f"Connected to {ps5_controller_address}")

        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type == "Key":
                    if event.code == "BTN_SOUTH" and event.state == 1:  # X button
                        await send_command_to_esp32("D2_toggle")
                    elif event.code == "BTN_EAST" and event.state == 1:  # Circle button
                        await send_command_to_esp32("D3_toggle")
                    elif event.code == "BTN_WEST" and event.state == 1:  # Square button
                        await send_command_to_esp32("D4_toggle")
                    elif event.code == "BTN_NORTH" and event.state == 1:  # Triangle button
                        await send_command_to_esp32("D5_toggle")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_ps5_controller())