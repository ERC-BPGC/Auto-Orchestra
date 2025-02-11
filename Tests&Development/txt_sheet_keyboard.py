import time
import serial

# Updated note mapping for 2nd, 3rd, and 4th octaves
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


def calculate_delay(velocity):
    min_delay = 100  # Minimum delay in ms
    max_delay = 500  # Maximum delay in ms
    delay = (min_delay + (max_delay - min_delay) * (127 - velocity) / 127)
    return int(delay)

def play_notes_from_file(file_path):
    arduino = serial.Serial(port='/dev/tty.usbmodem1301', baudrate=9600, timeout=1)
    
    with open(file_path, 'r') as file:
        for line in file:
            notes = line.strip().split(', ')
            for note_group in notes:
                for note in note_group.split():
                    if note in note_map:
                        servo_no = note_map[note]["keyboard_servo"]
                        servo_direction = note_map[note]["keyboard_direction"]
                        
                        # Press the note
                        delay = calculate_delay(100)  # Using a default velocity of 100
                        output = f"{servo_no:02}{delay:04}{servo_direction}"
                        print(f"Note {note} pressed: Output Code = {output}")
                        arduino.write((output + "\n").encode())
                        time.sleep(delay / 1000.0)
                        
                        # Release the note
                        servo_direction = 1 - servo_direction
                        output = f"{servo_no:02}{delay:04}{servo_direction}"
                        print(f"Note {note} released: Output Code = {output}")
                        arduino.write((output + "\n").encode())
                        time.sleep(delay / 1000.0)
                
                # Add a small delay between note groups
                time.sleep(0.1)
    
    arduino.close()

# Example usage
play_notes_from_file("/Users/sudhanshukulkarni/projects/Auto_Orchestra/Natarang.txt")
