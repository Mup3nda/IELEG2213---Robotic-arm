import asyncio
from ps5_controller import connect_ps5_controller
from m_Control.lib.preBLE.esp32_ble_control import connect_to_esp32, disconnect_from_esp32

async def main():
    await connect_to_esp32()
    await connect_ps5_controller()
    await disconnect_from_esp32()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())