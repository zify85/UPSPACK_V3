#!/usr/bin/python3

import os
import time
from threading import Thread
from UPS_GUI_py import UPS2

# Script to monitor power loss and log events using a UART connection to a UPS device.

def write_log(message):
    with open("/home/pi/powerloss_log.txt", "a+") as f:
        f.write(message)

def powerloss_check():
    print("start powerloss check")
    uart_data = UPS2("/dev/ttyAMA0")

    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    start_time = "Start time :"+cur_time + "\n"

    write_log(start_time)

    while True:
        version, vin, batcap, vout = uart_data.decode_uart()
        time.sleep(1)  # Check every 1s
        
        # If power is connected, continue monitoring
        if vin != "NG":
            print("Power connected, monitoring...")
            continue
        
        # Power loss detected - start counting
        print("Power loss detected, starting timer...")
        cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        power_loss_log = f"Power loss detected at: {cur_time}\n"
        write_log(power_loss_log)
        
        power_loss_time = 0
        
        while vin == "NG":  # While power is still lost
            time.sleep(1)  # Wait 1 second
            power_loss_time += 1
            print(f"Power lost for {power_loss_time} seconds")
            
            # Check if power loss exceeds 60 seconds
            if power_loss_time >= 60:
                cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                shutdown_log = f"Power loss exceeded 60 seconds at: {cur_time}, shutting down...\n"
                write_log(shutdown_log)
                break
            
            # Check power status again
            version, vin, batcap, vout = uart_data.decode_uart()
        
        # If we broke out due to 60+ second power loss, shutdown
        if power_loss_time >= 60:
            break
        else:
            print(f"Power restored after {power_loss_time} seconds, resetting counter")
            cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            power_restore_log = f"Power restored at: {cur_time} (after {power_loss_time} seconds)\n"
            write_log(power_restore_log)

    print("active halt...")
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    stop_time = "active halt...Halt time :"+ cur_time + "\n\n"
    write_log(stop_time)
    os.system("sudo sync")
    time.sleep(1)
    os.system("sudo shutdown now -h")

if __name__ == "__main__":
    try:
        t1 = Thread( target = powerloss_check )
        t1.start()
    except:
        t1.stop()
        GPIO.cleanup()

