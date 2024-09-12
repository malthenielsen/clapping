import numpy as np
from matplotlib import pyplot as plt
plt.style.use('K_PAPER')
import time
import numpy as np
import sounddevice as sd
from pynput import keyboard
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', "--opts",)    
args = parser.parse_args()
print(args.opts)

# Initialize variables
press_times = []
total_strokes = 50  # Set the number of strokes to track
frequency = 500  # Frequency of the sound in Hertz
duration = 0.1  # Duration of each sound chunk in seconds
sound_period = float(args.opts)
keep_playing = True  # Flag to keep sound playing in background

# Function to play sound continuously in the background
def play_background_sound():
    global sound_period
    samplerate = 44100  # Standard audio sample rate
    t = np.linspace(0, duration, int(samplerate * duration), False)
    wave = np.sin(frequency * 2 * np.pi * t)
    
    while keep_playing:
        sd.play(wave, samplerate)
        sd.wait()  # Wait for the chunk to finish playing
        time.sleep(max(0, sound_period - duration))


# Define the callback for key presses
def on_press(key):
    global press_times, sound_period
    try:
        if key == keyboard.Key.space:  # Detect spacebar press
            current_time = time.time()
            press_times.append(current_time)
            print(f"Spacebar pressed {len(press_times)} times.")
            #  sound_period -= 0.02
            #  if len(press_times)%15 == 0:
                #  sound_period -= .2
            #  if len(press_times) > 1:
                #  sound_period = press_times[-1] - press_times[-2]
            
            if len(press_times) >= total_strokes:
                return False  # Stop listener after 50 presses
    except AttributeError:
        pass

def main():
    print(f"Press the spacebar {total_strokes} times to measure the time between presses.")
    
    # Start the background sound in a separate thread
    sound_thread = threading.Thread(target=play_background_sound)
    sound_thread.start()
    
    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Wait until the user presses the spacebar 50 times
    
    # Stop the sound thread after spacebar presses
    global keep_playing
    keep_playing = False
    sound_thread.join()  # Wait for the sound thread to finish

    # Calculate and display the time between each press
    if len(press_times) > 1:
        print("\nTime between each spacebar press:")
        for i in range(1, len(press_times)):
            time_diff = press_times[i] - press_times[i - 1]
            print(f"Press {i}: {time_diff:.2f} seconds")
        np.save('perturbed_frequency', press_times)
        fig, ax = plt.subplots(1,2, figsize = (10,7))
        ax[0].plot(np.diff(press_times))
        ax[0].hlines(1, 0, 49, color = 'black')
        ax[1].hist(np.diff(press_times), bins = 10)
        plt.show()

    else:
        print("Not enough presses to measure time intervals.")

if __name__ == "__main__":
    main()


