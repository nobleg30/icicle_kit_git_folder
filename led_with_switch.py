import time
import os

# GPIO configuration
INPUT_PIN = 519   # Pin number for the input
OUTPUT_PIN = 526  # Pin number for the LED
GPIO_PATH = "/sys/class/gpio"
EXPORT_PATH = f"{GPIO_PATH}/export"
UNEXPORT_PATH = f"{GPIO_PATH}/unexport"

def setup_gpio(pin, direction):
    gpio_path = f"{GPIO_PATH}/gpio{pin}"
    
    # Export the GPIO pin
    if not os.path.exists(gpio_path):
        with open(EXPORT_PATH, 'w') as f:
            f.write(str(pin))
    
    # Set the direction
    with open(f"{gpio_path}/direction", 'w') as f:
        f.write(direction)

def cleanup_gpio(pin):
    gpio_path = f"{GPIO_PATH}/gpio{pin}"
    # Unexport the GPIO pin
    if os.path.exists(gpio_path):
        with open(UNEXPORT_PATH, 'w') as f:
            f.write(str(pin))

def read_gpio(pin):
    gpio_path = f"{GPIO_PATH}/gpio{pin}/value"
    with open(gpio_path, 'r') as f:
        return f.read().strip() == "1"

def write_gpio(pin, value):
    gpio_path = f"{GPIO_PATH}/gpio{pin}/value"
    with open(gpio_path, 'w') as f:
        f.write(str(value))

def monitor_input_and_control_led(input_pin, output_pin):
    try:
        # Set up the pins
        setup_gpio(input_pin, "in")
        setup_gpio(output_pin, "out")
        
        print("Monitoring input pin...")
        while True:
            # Read the input pin
            input_state = read_gpio(input_pin)
            
            # Control the LED based on input state
            if input_state:
                write_gpio(output_pin, 1)  # Turn LED on
                print("Input HIGH: LED ON")
            else:
                write_gpio(output_pin, 0)  # Turn LED off
                print("Input LOW: LED OFF")
            
            time.sleep(0.1)  # Polling interval
    finally:
        # Cleanup GPIO pins
        cleanup_gpio(input_pin)
        cleanup_gpio(output_pin)

if __name__ == "__main__":
    print("Starting GPIO monitor...")
    monitor_input_and_control_led(INPUT_PIN, OUTPUT_PIN)
