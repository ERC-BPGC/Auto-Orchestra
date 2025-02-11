

import mido
import time
import serial

# Mapping MIDI notes to servos based on the new specification
note_map = {
    # C3 to B3 (MIDI notes 48 to 59) white keys
    "C3": {"midi": 48, "keyboard_servo": 1, "keyboard_direction": 0},
    "D3": {"midi": 50, "keyboard_servo": 1, "keyboard_direction": 1},
    "E3": {"midi": 52, "keyboard_servo": 2, "keyboard_direction": 0},
    "F3": {"midi": 53, "keyboard_servo": 2, "keyboard_direction": 1},
    "G3": {"midi": 55, "keyboard_servo": 3, "keyboard_direction": 0},
    "A3": {"midi": 57, "keyboard_servo": 3, "keyboard_direction": 1},
    "B3": {"midi": 59, "keyboard_servo": 4, "keyboard_direction": 0},

    # Second octave white keys
    "C4": {"midi": 60, "keyboard_servo": 4, "keyboard_direction": 1},
    "D4": {"midi": 62, "keyboard_servo": 5, "keyboard_direction": 0},
    "E4": {"midi": 64, "keyboard_servo": 5, "keyboard_direction": 1},
    "F4": {"midi": 65, "keyboard_servo": 6, "keyboard_direction": 0},
    "G4": {"midi": 67, "keyboard_servo": 6, "keyboard_direction": 1},
    "A4": {"midi": 69, "keyboard_servo": 7, "keyboard_direction": 0},
    "B4": {"midi": 71, "keyboard_servo": 7, "keyboard_direction": 1},

    # Third octave white keys
    "C5": {"midi": 72, "keyboard_servo": 8, "keyboard_direction": 0},
    "D5": {"midi": 74, "keyboard_servo": 8, "keyboard_direction": 1},
    "E5": {"midi": 76, "keyboard_servo": 9, "keyboard_direction": 0},
    "F5": {"midi": 77, "keyboard_servo": 9, "keyboard_direction": 1},
    "G5": {"midi": 79, "keyboard_servo": 10, "keyboard_direction": 0},
    "A5": {"midi": 81, "keyboard_servo": 10, "keyboard_direction": 1},
    "B5": {"midi": 83, "keyboard_servo": 11, "keyboard_direction": 0},

    # Black keys first octave
    "C#3": {"midi": 49, "keyboard_servo": 12, "keyboard_direction": 1},
    "D#3": {"midi": 51, "keyboard_servo": 12, "keyboard_direction": 0},
    "F#3": {"midi": 54, "keyboard_servo": 13, "keyboard_direction": 1},
    "G#3": {"midi": 56, "keyboard_servo": 13, "keyboard_direction": 0},
    "A#3": {"midi": 58, "keyboard_servo": 14, "keyboard_direction": 1},

    # Black keys second octave
    "C#4": {"midi": 61, "keyboard_servo": 14, "keyboard_direction": 0},
    "D#4": {"midi": 63, "keyboard_servo": 15, "keyboard_direction": 1},
    "F#4": {"midi": 66, "keyboard_servo": 15, "keyboard_direction": 0},
    "G#4": {"midi": 68, "keyboard_servo": 16, "keyboard_direction": 1},
    "A#4": {"midi": 70, "keyboard_servo": 16, "keyboard_direction": 0},

    # Black keys third octave
    "C#5": {"midi": 73, "keyboard_servo": 17, "keyboard_direction": 0},
    "D#5": {"midi": 75, "keyboard_servo": 17, "keyboard_direction": 1},
    "F#5": {"midi": 78, "keyboard_servo": 18, "keyboard_direction": 0},
    "G#5": {"midi": 80, "keyboard_servo": 18, "keyboard_direction": 1},
    "A#5": {"midi": 82, "keyboard_servo": 19, "keyboard_direction": 0},
}


# Function to calculate delay based on velocity
def calculate_delay(velocity):
    min_delay = 100  # Minimum delay in ms
    max_delay = 500  # Maximum delay in ms
    delay = (min_delay + (max_delay - min_delay) * (127 - velocity) / 127)
    return int(delay)

# Function to play MIDI file and send servo instructions to Arduino
def play_midi_from_file(midi_file_path):
    # Open serial connection to Arduino
    #arduino = serial.Serial(port= '/dev/tty.usbmodem21201', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino port

    midi_file = mido.MidiFile(midi_file_path)

    for msg in midi_file.play():
        print(msg)
        if msg.type == 'note_on' or msg.type == 'note_off':
            note = msg.note
            #print(msg.velocity)
            velocity = msg.velocity

            if note in note_map:
                keyboard_note = note_map[note]["key"]
                servo_no = note_map[note]["servo"]
                action = "pressed" if msg.type == 'note_on' else "released"

                # Determine servo direction
                servo_direction = note_map[note]["servo_direction"]
                if msg.type == 'note_off':
                    servo_direction = 1 - servo_direction  # Reverse direction for release

                # Calculate delay
                delay = calculate_delay(velocity)

                # Format output
                output = f"{servo_no:02}{delay:04}{servo_direction}"
                #print(f"Note {keyboard_note} {action}: Output Code = {output}")

                # Send data to Arduino
                #arduino.write((output + "\n").encode())  # Send output with a newline character

                # Simulate the action with a delay
                time.sleep(delay / 1000.0)

    # Close the serial connection
   # arduino.close()

# Example usage
play_midi_from_file(r"/Users/sudhanshukulkarni/projects/Auto_Orchestra/Unravel Tokyo Ghoul Piano Cover MIDI.mid")
