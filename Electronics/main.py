import time
import pins

def main():
    """Main function to handle user interaction."""
    try:
        pins.startup_sequence()
        while True:
            user_input = input("Enter pin position (e.g., 1A, 2B) to toggle or 'q' to quit: ").upper()
            if user_input == 'Q':
                break
            elif user_input in pins.PIN_CONFIG:
                pins.set_pin(user_input, True)
                time.sleep(1)
                pins.set_pin(user_input, False)
            else:
                print("Invalid input. Please enter a valid pin position.")
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        pins.cleanup()
        print("GPIO cleaned up. Goodbye!")

if __name__ == "__main__":
    main()