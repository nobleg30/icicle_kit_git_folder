import serial

# Configure UART
uart = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Replace with the correct UART device
try:
    # Send command to HMI
    uart.write(b't0.txt="Noble G"\xFF\xFF\xFF')
    uart.write(b'b0.txt="Hello"\xFF\xFF\xFF')
    uart.write(b'qr0.txt="https://www.manoramaonline.com/"\xFF\xFF\xFF')
    print("Command sent to HMI.")
except Exception as e:
    print(f"Error: {e}")
finally:
    uart.close()
