import time
import os

# Pin configuration
DT_PIN = 518  # GPIO number for HX711 DT (example GPIO_2_5)
SCK_PIN = 519  # GPIO number for HX711 SCK
LED_PIN = 517  # GPIO number for LED

# Helper functions for GPIO management
def export_gpio(pin):
    if not os.path.exists(f"/sys/class/gpio/gpio{pin}"):
        with open("/sys/class/gpio/export", "w") as f:
            f.write(str(pin))

def unexport_gpio(pin):
    if os.path.exists(f"/sys/class/gpio/gpio{pin}"):
        with open("/sys/class/gpio/unexport", "w") as f:
            f.write(str(pin))

def set_gpio_direction(pin, direction):
    with open(f"/sys/class/gpio/gpio{pin}/direction", "w") as f:
        f.write(direction)

def write_gpio(pin, value):
    with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
        f.write(str(value))

def read_gpio(pin):
    with open(f"/sys/class/gpio/gpio{pin}/value", "r") as f:
        return int(f.read().strip())

# GPIO setup
export_gpio(DT_PIN)
export_gpio(SCK_PIN)
export_gpio(LED_PIN)
set_gpio_direction(DT_PIN, "in")
set_gpio_direction(SCK_PIN, "out")
set_gpio_direction(LED_PIN, "out")

def read_raw_data():
    """Reads raw data from the HX711."""
    data = 0
    write_gpio(SCK_PIN, 0)

    # Wait until DT pin is LOW
    while read_gpio(DT_PIN):
        pass

    # Read 24 bits of data
    for i in range(24):
        write_gpio(SCK_PIN, 1)
        data = (data << 1) | read_gpio(DT_PIN)
        write_gpio(SCK_PIN, 0)

    # Set the gain to 128 (default)
    write_gpio(SCK_PIN, 1)
    write_gpio(SCK_PIN, 0)

    # Convert from 2's complement
    if data & 0x800000:
        data -= 0x1000000

    return data

def get_weight(samples=10):
    """Calculates the average weight from a number of samples."""
    total = 0
    for _ in range(samples):
        total += read_raw_data()
        time.sleep(0.1)  # Small delay between samples
    return total / samples

def blink_led(times=5, interval=0.5):
    """Blinks the LED a specified number of times."""
    for _ in range(times):
        write_gpio(LED_PIN, 1)  # Turn LED on
        time.sleep(interval)
        write_gpio(LED_PIN, 0)  # Turn LED off
        time.sleep(interval)

try:
    print("Starting HX711 interface with LED blinking...")
    while True:
        # Blink the LED
        blink_led(times=1, interval=0.2)

        # Read weight from HX711
        weight = get_weight()
        print(f"Raw Data: {weight}")

        # Wait before next reading
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    unexport_gpio(DT_PIN)
    unexport_gpio(SCK_PIN)
    unexport_gpio(LED_PIN)

