import subprocess

def get_bluetooth_devices():
    # Run the PowerShell command
    result = subprocess.run(
        ["powershell", "-Command", "Get-PnpDevice -Class Bluetooth | Select-Object Name, Status, InstanceId"],
        capture_output=True,
        text=True
    )
    
    # Decode the output
    output = result.stdout
    
    # Split the output into lines
    lines = output.splitlines()
    
    # Skip the header line
    for line in lines[3:]:
        parts = line.split()
        if len(parts) >= 3:
            device_name = " ".join(parts[:-2])
            mac_address = parts[-1]
            print(f"DeviceName: {device_name}, MacAddress: {mac_address}")

# Call the function to get and print Bluetooth devices
get_bluetooth_devices()