#!/usr/bin/env python3
"""
Example script showing how to use the UPS_GUI_py package
"""

# Import the UPS classes from the package
from UPS_GUI_py import UPS2, UPS2_IO
import time

def main():
    """Main demo function"""
    print("UPS Package Demo")
    print("================")
    
    # Example 1: Basic UPS monitoring
    print("\n1. Basic UPS monitoring:")
    try:
        # Initialize UPS with serial port (adjust port as needed)
        ups = UPS2("/dev/ttyAMA0")
        
        print("Reading UPS data...")
        version, vin, batcap, vout = ups.decode_uart()
        
        print(f"UPS Version: {version}")
        print(f"Input Status: {'Connected' if vin != 'NG' else 'NOT Connected'}")
        print(f"Battery Capacity: {batcap}%")
        print(f"Output Voltage: {vout} mV")
        
    except Exception as e:
        print(f"Error connecting to UPS: {e}")
        print("Make sure the UPS is connected and the serial port is correct.")
    
    # Example 2: GPIO monitoring setup
    print("\n2. GPIO monitoring setup:")
    try:
        # Initialize GPIO monitoring (default pin 18)
        ups_io = UPS2_IO(bcm_io=18)
        print("GPIO monitoring initialized on BCM pin 18")
        print("The system will monitor for low battery shutdown signals.")
        
    except Exception as e:
        print(f"Error setting up GPIO monitoring: {e}")
        print("Make sure you're running on a Raspberry Pi with proper permissions.")

if __name__ == "__main__":
    main()
