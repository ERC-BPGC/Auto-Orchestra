# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b9bm4XKDsE9PQeJ09YqjtVySizoiI592
"""

pip install pydub numpy scipy librosa pretty_midi

import os
import numpy as np
import librosa
import pretty_midi
from pydub import AudioSegment

output_path = os.path.expanduser("~/Auto_Orchestra_output")
os.makedirs(output_path, exist_ok=True)

def MP3_to_WAV(mp3_file):
    """Convert MP3 to WAV format."""
    sound = AudioSegment.from_mp3(mp3_file)
    filename = os.path.basename(mp3_file).split('.')[0]  # Extract filename without extension
    wav_file_name = os.path.join(output_path, filename + ".wav")  # Full path for WAV file
    sound.export(wav_file_name, format="wav")
    return wav_file_name

def wav_to_midi(wav_file):
    """Convert WAV to MIDI using pitch detection."""
    # Load the WAV file
    y, sr = librosa.load(wav_file, sr=None, mono=True)

    # Extract pitch using librosa's piptrack
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    # Create a PrettyMIDI object
    midi_data = pretty_midi.PrettyMIDI()

    # Create an instrument instance (e.g., piano)
    instrument = pretty_midi.Instrument(program=0)  # Program 0 is Acoustic Grand Piano

    # Convert pitches to MIDI notes
    for frame in range(pitches.shape[1]):
        pitch_index = magnitudes[:, frame].argmax()
        pitch = pitches[pitch_index, frame]
        if pitch > 0:  # Ignore silent frames
            # Convert frequency to MIDI note number
            midi_note = librosa.hz_to_midi(pitch)
            # Create a note instance
            note = pretty_midi.Note(
                velocity=100,  # Note velocity (loudness)
                pitch=int(midi_note),  # MIDI note number
                start=frame * 0.1,  # Start time (in seconds)
                end=(frame + 1) * 0.1  # End time (in seconds)
            )
            instrument.notes.append(note)

    # Add the instrument to the PrettyMIDI object
    midi_data.instruments.append(instrument)

    # Save the MIDI file
    midi_file_name = os.path.join(output_path, os.path.basename(wav_file).split('.')[0] + ".midi")
    midi_data.write(midi_file_name)
    return midi_file_name

# Example usage
mp3_file = "/Users/sudhanshukulkarni/projects/Auto_Orchestra/happy-birthday-254480.mp3"  # Change this to your MP3 file path

# Step 1: Convert MP3 to WAV
wav_file = MP3_to_WAV(mp3_file)
print(f"Converted WAV file saved at: {wav_file}")

# Step 2: Convert WAV to MIDI
midi_file = wav_to_midi(wav_file)
print(f"Converted MIDI file saved at: {midi_file}")

import mido
import time
import serial

# Updated flute patterns as per your specifications
note_map = {
    # C3 to B3 (MIDI notes 48 to 59) white keys
    48:{"key": "C3", "keyboard_servo":1, "keyboard_direction":0},  # C3
    50:{"key": "D3", "keyboard_servo":1, "keyboard_direction":1},  # D3
    52:{"key": "E3", "keyboard_servo":2, "keyboard_direction":0},  # E3
    53:{"key": "F3", "keyboard_servo":2, "keyboard_direction":1},  # F3
    55:{"key": "G3", "keyboard_servo":3, "keyboard_direction":0},  # G3
    57:{"key": "A3", "keyboard_servo":3, "keyboard_direction":1},  # A3
    59:{"key": "B3", "keyboard_servo":4, "keyboard_direction":0},  # B3

    #second octave white keys
    60:{"key": "C4", "keyboard_servo":4, "keyboard_direction":1},  # C4
    62:{"key": "D4", "keyboard_servo":5, "keyboard_direction":0},  # D4
    64:{"key": "E4", "keyboard_servo":5, "keyboard_direction":1},  # E4
    65:{"key": "F4", "keyboard_servo":6, "keyboard_direction":0},  # F4
    67:{"key": "G4", "keyboard_servo":6, "keyboard_direction":1},  # G4
    69:{"key": "A4", "keyboard_servo":7, "keyboard_direction":0},  # A4
    71:{"key": "B4", "keyboard_servo":7, "keyboard_direction":1},  # B4

    # third octave white keys
    72:{"key": "C5", "keyboard_servo":8, "keyboard_direction":0},  # C5
    74:{"key": "D5", "keyboard_servo":8, "keyboard_direction":1},  # D5
    76:{"key": "E5", "keyboard_servo":9, "keyboard_direction":0},  # E5
    77:{"key": "F5", "keyboard_servo":9, "keyboard_direction":1},  # F5
    79:{"key": "G5", "keyboard_servo":10,"keyboard_direction":0},  # G5
    81:{"key": "A5", "keyboard_servo":10,"keyboard_direction":1},  # A5
    83:{"key": "B5", "keyboard_servo":11,"keyboard_direction":0},  # B5

    #black keys first octave
    49:{"key": "C#3", "keyboard_servo":12, "keyboard_direction":1},  # C#3
    51:{"key": "D#3", "keyboard_servo":12, "keyboard_direction":0},  # D#3
    54:{"key": "F#3", "keyboard_servo":13, "keyboard_direction":1},  # F#3
    56:{"key": "G#3", "keyboard_servo":13, "keyboard_direction":0},  # G#3
    58:{"key": "A#3", "keyboard_servo":14, "keyboard_direction":1},  # A#3

    #black keys second octave
    61:{"key": "C#4", "keyboard_servo":14, "keyboard_direction":0},  # C#4
    63:{"key": "D#4", "keyboard_servo":15, "keyboard_direction":1},  # D#4
    66:{"key": "F#4", "keyboard_servo":15, "keyboard_direction":0},  # F#4
    68:{"key": "G#4", "keyboard_servo":16, "keyboard_direction":1},  # G#4
    70:{"key": "A#4", "keyboard_servo":16, "keyboard_direction":0},  # A#4

    # black keys third octave
    73:{"key": "C#5", "keyboard_servo":17, "keyboard_direction":0},  # C#5
    75:{"key": "D#5", "keyboard_servo":17, "keyboard_direction":1},  # D#5
    78:{"key": "F#5", "keyboard_servo":18, "keyboard_direction":0},  # F#5
    80:{"key": "G#5", "keyboard_servo":18, "keyboard_direction":1,},  # G#5
    82:{"key": "A#5", "keyboard_servo":19, "keyboard_direction":0},  # A#5
}

# Function to calculate delay based on velocity
def calculate_delay(velocity):
    min_delay = 100  # Minimum delay in ms
    max_delay = 500  # Maximum delay in ms
    delay = min_delay + (max_delay - min_delay) * (127 - velocity) / 127
    return int(delay)

# Function to play MIDI file and send servo instructions to Arduino
def play_midi_from_file(midi_file_path):
    arduino = serial.Serial(port='/dev/tty.usbmodem21301', baudrate=9600, timeout=0.1)  # Update with your Arduino port
    midi_file = mido.MidiFile(midi_file_path)

    for msg in midi_file.play():
        if msg.type == 'note_on' or msg.type == 'note_off':
            note = msg.note
            velocity = msg.velocity

            if note in note_map:
                keyboard_note = note_map[note]["key"]
                servo_no = note_map[note]["keyboard_servo"]
                action = "pressed" if msg.type == 'note_on' else "released"

                # Determine servo direction
                servo_direction = note_map[note]["keyboard_direction"]
                if msg.type == 'note_off':
                    servo_direction = 1 - servo_direction  # Reverse direction for release

                # Get flute pattern
                flute_pattern = note_map[note]["flute_pattern"]

                # Combine output into a 9-digit code
                output = f"{servo_no:02}{servo_direction}{flute_pattern}"
                print(f"Note {keyboard_note} {action}: Output Code = {output}")

                # Send data to Arduino
                arduino.write((output + "\n").encode())

                # Simulate the action with a delay
                time.sleep(calculate_delay(velocity) / 1000.0)

    arduino.close()

# Example usage
play_midi_from_file(midi_file)