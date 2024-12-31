import serial
import time

def read_uart():
    try:
        # Attempt to open UART connection
        ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)
        print(f"Listening on {ser.port} at {ser.baudrate} baud rate")
    except serial.SerialException as e:
        print(f"Error opening UART: {e}")
        return

    try:
        while True:
            try:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    print(f"Received: {data}")
            except UnicodeDecodeError:
                print("Received non-decodable data")
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                break
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if ser.is_open:
            ser.close()
            print("UART connection closed.")

if __name__ == "__main__":
    read_uart()
