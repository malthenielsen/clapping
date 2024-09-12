import numpy as np
from matplotlib import pyplot as plt
plt.style.use('K_PAPER')
from pynput import keyboard
import time

# Initialize variables
press_times = []
total_strokes = 50  # Set the number of strokes to track

# Define the callback for key presses
def on_press(key):
    try:
        if key == keyboard.Key.space:  # Detect spacebar press
            current_time = time.time()
            press_times.append(current_time)
            print(f"Spacebar pressed {len(press_times)} times.")
            
            if len(press_times) >= total_strokes:
                return False  # Stop listener after 50 presses
    except AttributeError:
        pass

def main():
    print(f"Press the spacebar {total_strokes} times to measure the time between presses.")
    
    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Wait until the user presses the spacebar 50 times

    # Calculate and display the time between each press
    if len(press_times) > 1:
        print("\nTime between each spacebar press:")
        for i in range(1, len(press_times)):
            time_diff = press_times[i] - press_times[i - 1]
            print(f"Press {i}: {time_diff:.2f} seconds")
        np.save('eigen_press', press_times)
        print(np.mean(np.diff(press_times)))
    else:
        print("Not enough presses to measure time intervals.")

if __name__ == "__main__":
    main()


