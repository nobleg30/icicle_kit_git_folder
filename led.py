import time
import os

# GPIO configuration
GPIO_PIN = 515  # Pin number where LED is connected
GPIO_PATH = f"/sys/class/gpio/gpio{GPIO_PIN}"
EXPORT_PATH = "/sys/class/gpio/export"
UNEXPORT_PATH = "/sys/class/gpio/unexport"

def setup_gpio(pin):
    # Export the GPIO pin
    if not os.path.exists(GPIO_PATH):
        with open(EXPORT_PATH, 'w') as f:
            f.write(str(pin))
    
    # Set the direction to "out"
    with open(f"{GPIO_PATH}/direction", 'w') as f:
        f.write("out")

def cleanup_gpio(pin):
    # Unexport the GPIO pin
    if os.path.exists(GPIO_PATH):
        with open(UNEXPORT_PATH, 'w') as f:
            f.write(str(pin))

def blink_led(pin, interval=1.0, times=10):
    try:
        setup_gpio(pin)
        for _ in range(times):
            # Turn LED on
            with open(f"{GPIO_PATH}/value", 'w') as f:
                f.write("1")
            time.sleep(interval)
            
            # Turn LED off
            with open(f"{GPIO_PATH}/value", 'w') as f:
                f.write("0")
            time.sleep(interval)
    finally:
        cleanup_gpio(pin)

if __name__ == "__main__":
    print("Blinking LED on GPIO26...")
    blink_led(GPIO_PIN, interval=0.5, times=20)  # Adjust interval and times as needed
    print("Done.")
