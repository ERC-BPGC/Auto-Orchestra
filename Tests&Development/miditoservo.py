import mido
import time
import serial

# Mapping MIDI notes to servos based on the new specification
note_map = {
    60: {"key": "C4", "servo": 1, "servo_direction": 0},  # C4
    62: {"key": "D4", "servo": 1, "servo_direction": 1},  # D4
    64: {"key": "E4", "servo": 2, "servo_direction": 0},  # E4
    65: {"key": "F4", "servo": 2, "servo_direction": 1},  # F4
    67: {"key": "G4", "servo": 3, "servo_direction": 0},  # G4
    69: {"key": "A4", "servo": 3, "servo_direction": 1},  # A4
    61: {"key": "C#4", "servo": 4, "servo_direction": 0},  # C#4
    63: {"key": "D#4", "servo": 4, "servo_direction": 1},  # D#4
    66: {"key": "F#4", "servo": 5, "servo_direction": 0},  # F#4
    68: {"key": "G#4", "servo": 5, "servo_direction": 1},  # G#4
    71: {"key": "B4", "servo": 6, "servo_direction": 0},  # B4
    72: {"key": "B#4", "servo": 6, "servo_direction": 1},  # B#4
}

# Function to calculate delay based on velocity
def calculate_delay(velocity):
    min_delay = 100  # Minimum delay in ms
    max_delay = 500  # Maximum delay in ms
    delay = min_delay + (max_delay - min_delay) * (127 - velocity) / 127
    return int(delay)

# Function to play MIDI file and send servo instructions to Arduino
def play_midi_from_file(midi_file_path):
    # Open serial connection to Arduino
    arduino = serial.Serial(port= '/dev/tty.usbmodem21301', baudrate=9600, timeout=0.1)  # Replace 'COM3' with your Arduino port

    midi_file = mido.MidiFile(midi_file_path)

    for msg in midi_file.play():
        if msg.type == 'note_on' or msg.type == 'note_off':
            note = msg.note
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
                print(f"Note {keyboard_note} {action}: Output Code = {output}")

                # Send data to Arduino
                arduino.write((output + "\n").encode())  # Send output with a newline character

                # Simulate the action with a delay
                time.sleep(delay / 1000.0)

    # Close the serial connection
    arduino.close()

# Example usage
play_midi_from_file(r"/Users/sudhanshukulkarni/projects/Auto_Orchestra/Unravel Tokyo Ghoul Piano Cover MIDI.mid")