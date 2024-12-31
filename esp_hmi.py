import serial
import time

# Configure UART
uart = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Replace with the correct UART device

def read_and_update_hmi():
    try:
        print(f"Listening on {uart.port} at {uart.baudrate} baud rate")
        while True:
            data = uart.readline().decode('utf-8', errors='ignore').strip()  # Handle decoding errors gracefully
            if data.startswith("Weight:"):
                try:
                    # Extract the weight value
                    weight = data.split(":")[1].strip().split(" ")[0]
                    print(f"Parsed Weight: {weight}")

                    # Prepare the HMI commands
                    weight_command = bytearray(f't0.txt="{weight}"', 'utf-8') + b'\xFF\xFF\xFF'
                    message_command = bytearray('b0.txt="Weight received"', 'utf-8') + b'\xFF\xFF\xFF'

                    # Send commands to HMI
                    uart.write(weight_command)  # Update t0 with weight
                    uart.write(message_command)  # Update b0 with a message

                    print(f"Sent to HMI: {weight_command}")
                    print(f"Sent to HMI: {message_command}")
                except (IndexError, ValueError) as parse_error:
                    print(f"Parsing error: {parse_error}, raw data: {data}")
            else:
                print(f"Ignored invalid data: {data}")

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        uart.close()
        print("UART connection closed.")

if __name__ == "__main__":
    read_and_update_hmi()
