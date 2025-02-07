import RPi.GPIO as GPIO
import time

# Define GPIO pins in a structured way
PIN_CONFIG = {
    '1A': 11, '1B': 12,  # GPIO17, GPIO18
    '2A': 13, '2B': 16,  # GPIO27, GPIO23
    '3A': 15, '3B': 18,  # GPIO22, GPIO24
    '4A': 19, '4B': 22,  # GPIO10, GPIO25
    '5A': 21, '5B': 24,  # GPIO9, GPIO8
    '6A': 23, '6B': 26   # GPIO11, GPIO7
}

# Setup GPIO mode
GPIO.setmode(GPIO.BOARD)
for pin in PIN_CONFIG.values():
    GPIO.setup(pin, GPIO.OUT)

def set_pin(position, state):
    """Sets the given pin position to HIGH or LOW."""
    if position in PIN_CONFIG:
        GPIO.output(PIN_CONFIG[position], GPIO.HIGH if state else GPIO.LOW)

def cleanup():
    """Cleans up GPIO settings."""
    GPIO.cleanup()

def startup_sequence():
    """Runs the startup sequence."""
    # Turn on all LEDs for 3 seconds
    for pin in PIN_CONFIG.values():
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(3)

    # Turn off all LEDs for 1 second
    for pin in PIN_CONFIG.values():
        GPIO.output(pin, GPIO.LOW)
    time.sleep(1)

    # Turn each column on for 2 seconds and off for 1 second
    for col in ['A', 'B']:
        for row in range(1, 7):
            GPIO.output(PIN_CONFIG[f'{row}{col}'], GPIO.HIGH)
        time.sleep(2)
        for row in range(1, 7):
            GPIO.output(PIN_CONFIG[f'{row}{col}'], GPIO.LOW)
        time.sleep(1)

    # Test each pin one by one
    for position in PIN_CONFIG.keys():
        GPIO.output(PIN_CONFIG[position], GPIO.HIGH)
        time.sleep(1)
        GPIO.output(PIN_CONFIG[position], GPIO.LOW)
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        startup_sequence()
        while True:
            user_input = input("Enter pin position (e.g., 1A, 2B) to toggle or 'q' to quit: ").upper()
            if user_input == 'Q':
                break
            elif user_input in PIN_CONFIG:
                set_pin(user_input, True)
                time.sleep(1)
                set_pin(user_input, False)
            else:
                print("Invalid input. Please enter a valid pin position.")
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        cleanup()
        print("GPIO cleaned up. Goodbye!")