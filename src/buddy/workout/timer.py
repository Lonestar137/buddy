import time

import click
import sounddevice as sd
import numpy as np

# Generate a piano-like tone with decay
def generate_tone(frequency: int, duration: float, fs: int, volume: float):
    t = np.linspace(0, duration, int(fs * duration), False)
    # Sine wave with exponential decay for piano-like sound
    audio = volume * np.sin(2 * np.pi * frequency * t) * np.exp(-t * 4)
    return audio.astype(np.float32)

@click.group()
def workout():
    pass

@workout.command()
@click.option('-f', '--sample-rate', type=int, default=44100)
@click.option('-d', '--duration', type=float, default=0.5)
@click.option('-v', '--volume', type=float, default=0.5)
@click.option('-r', '--runtime', type=int, default=1800)
@click.option('-i', '--interval', type=int, default=30)
def timer(sample_rate: int, duration: float, volume: float, runtime: int, interval: int) -> None:

    # Melody: Frequencies for "Twinkle, Twinkle, Little Star" (C, C, G, G, A, A, G)
    melody_frequencies = [
        261.63,  # C4 (Middle C)
        261.63,  # C4
        391.99,  # G4
        391.99,  # G4
        440.00,  # A4
        440.00,  # A4
        391.99   # G4
    ]

    # Pre-generate all tones for the melody
    tones = [generate_tone(freq, duration, sample_rate, volume) for freq in melody_frequencies]
    melody_length = len(melody_frequencies)

    print(f"Starting {runtime}-minute melodic piano tone sequence...")
    start_time = time.time()
    elapsed = 0
    note_index = 0
    pretty_elapsed = elapsed
    try:
        while elapsed < runtime:
            pretty_elapsed = round(elapsed / 60, 2)
            current_freq = melody_frequencies[note_index]
            print(f"Playing note {note_index + 1}/{melody_length} (Freq: {current_freq:.2f} Hz) at {pretty_elapsed} minutes")
            sd.play(tones[note_index], sample_rate)
            sd.wait()  # Wait for the tone to finish playing
            time.sleep(interval - duration)  # Adjust sleep to maintain 30s interval
            elapsed = time.time() - start_time
            note_index = (note_index + 1) % melody_length  # Cycle through melody

        print(f"Finished {pretty_elapsed}-minute sequence.")
    except KeyboardInterrupt:
        print("Keyboard interrupt caught.")
        print("Elapsed: ", pretty_elapsed)


