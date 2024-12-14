import time
import os
import threading

LED_GPIO = 517
TRIG_GPIO = 522
ECHO_GPIO = 527
ECHO_TIMEOUT = 0.02  # 20 ms (timeout for ECHO response)

def gpio_path(gpio_number, file):
    return f"/sys/class/gpio/gpio{gpio_number}/{file}"

def export_gpio(gpio_number):
    if not os.path.exists(f"/sys/class/gpio/gpio{gpio_number}"):
        with open("/sys/class/gpio/export", "w") as f:
            f.write(str(gpio_number))

def set_gpio_direction(gpio_number, direction):
    with open(gpio_path(gpio_number, "direction"), "w") as f:
        f.write(direction)

def write_gpio_value(gpio_number, value):
    with open(gpio_path(gpio_number, "value"), "w") as f:
        f.write(str(value))

def read_gpio_value(gpio_number):
    with open(gpio_path(gpio_number, "value"), "r") as f:
        return f.read().strip()

def unexport_gpio(gpio_number):
    if os.path.exists(f"/sys/class/gpio/gpio{gpio_number}"):
        with open("/sys/class/gpio/unexport", "w") as f:
            f.write(str(gpio_number))

def blink_led():
    while True:
        try:
            write_gpio_value(LED_GPIO, 1)
            time.sleep(0.5)
            write_gpio_value(LED_GPIO, 0)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error in LED blinking: {e}")
            break

def measure_distance():
    # Send 10 µs HIGH pulse to TRIG
    write_gpio_value(TRIG_GPIO, 1)
    time.sleep(0.00001)  # 10 µs
    write_gpio_value(TRIG_GPIO, 0)

    # Wait for ECHO to go HIGH with timeout
    start_time = time.time()
    timeout_start = time.time()
    while read_gpio_value(ECHO_GPIO) == "0":
        if time.time() - timeout_start > ECHO_TIMEOUT:
            print("ECHO signal timeout (waiting for HIGH)")
            return -1  # Indicate an error

    # Measure how long ECHO is HIGH with timeout
    start_time = time.time()
    timeout_start = time.time()
    while read_gpio_value(ECHO_GPIO) == "1":
        if time.time() - timeout_start > ECHO_TIMEOUT:
            print("ECHO signal timeout (stayed HIGH too long)")
            return -1  # Indicate an error

    # Calculate pulse duration and distance
    pulse_duration = (time.time() - start_time) * 1_000_000  # Convert to µs
    distance = pulse_duration / 58  # Distance in cm

    return distance

def main():
    export_gpio(LED_GPIO)
    print(f"Exported LED GPIO: {LED_GPIO}")
    export_gpio(TRIG_GPIO)
    print(f"Exported TRIG GPIO: {TRIG_GPIO}")
    export_gpio(ECHO_GPIO)
    print(f"Exported ECHO GPIO: {ECHO_GPIO}")
    set_gpio_direction(LED_GPIO, "out")
    set_gpio_direction(TRIG_GPIO, "out")
    set_gpio_direction(ECHO_GPIO, "in")

    # Start the LED blinking in a separate thread
    led_thread = threading.Thread(target=blink_led, daemon=True)
    led_thread.start()

    try:
        while True:
            distance = measure_distance()
            if distance == -1:
                print("Measurement error: Unable to determine distance.")
            else:
                print(f"Distance: {distance:.2f} cm")
            time.sleep(1)  # Delay before next measurement
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        unexport_gpio(LED_GPIO)
        unexport_gpio(TRIG_GPIO)
        unexport_gpio(ECHO_GPIO)
if __name__ == "__main__":
        main()

