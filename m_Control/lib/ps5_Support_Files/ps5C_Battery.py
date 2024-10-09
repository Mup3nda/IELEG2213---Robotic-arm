import hid
import time

# The vendor_id and product_id for the PS5 controller are 0x054C and 0x0CE6 respectively
vendor_id = 0x054C
product_id = 0x0CE6

try:
    device = hid.device()
    device.open(vendor_id, product_id)
    print("PS5 controller connected")

    # Query the battery level
    while True:
        report = device.read(64)
        if report:
            battery_level = report[53]  # The battery level is at byte 53 in the report
            print(f"Battery level: {battery_level}%")
        time.sleep(1)  # Add a 1-second delay
except IOError as e:
    print(f"Failed to connect to the PS5 controller: {e}")
finally:
    device.close()