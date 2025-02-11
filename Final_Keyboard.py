import tkinter as tk
from tkinter import filedialog
import serial
import time
import os
import mido

note_map = {
 48: {"key": "C3", "servo": 1, "servo_direction": 0},
    50: {"key": "D3", "servo": 1, "servo_direction": 1},
    52: {"key": "E3", "servo": 2, "servo_direction": 0},
    53: {"key": "F3", "servo": 2, "servo_direction": 1},
    55: {"key": "G3", "servo": 3, "servo_direction": 0},
    57: {"key": "A3", "servo": 3, "servo_direction": 1},
    59: {"key": "B3", "servo": 4, "servo_direction": 0},

    60: {"key": "C4", "servo": 4, "servo_direction": 1},
    62: {"key": "D4", "servo": 5, "servo_direction": 0},
    64: {"key": "E4", "servo": 5, "servo_direction": 1},
    65: {"key": "F4", "servo": 6, "servo_direction": 0},
    67: {"key": "G4", "servo": 6, "servo_direction": 1},
    69: {"key": "A4", "servo": 7, "servo_direction": 0},
    71: {"key": "B4", "servo": 7, "servo_direction": 1},

    72: {"key": "C5", "servo": 8, "servo_direction": 0},
    74: {"key": "D5", "servo": 8, "servo_direction": 1},
    76: {"key": "E5", "servo": 9, "servo_direction": 0},
    77: {"key": "F5", "servo": 9, "servo_direction": 1},
    79: {"key": "G5", "servo": 10, "servo_direction": 0},
    81: {"key": "A5", "servo": 10, "servo_direction": 1},
    83: {"key": "B5", "servo": 11, "servo_direction": 0},
    84: {"key": "C6", "servo": 11, "servo_direction": 1},

    49: {"key": "C#3", "servo": 12, "servo_direction": 1},
    51: {"key": "D#3", "servo": 12, "servo_direction": 0},
    54: {"key": "F#3", "servo": 13, "servo_direction": 1},
    56: {"key": "G#3", "servo": 13, "servo_direction": 0},
    58: {"key": "A#3", "servo": 14, "servo_direction": 1},

    61: {"key": "C#4", "servo": 14, "servo_direction": 0},
    63: {"key": "D#4", "servo": 15, "servo_direction": 1},
    66: {"key": "F#4", "servo": 15, "servo_direction": 0},
    68: {"key": "G#4", "servo": 16, "servo_direction": 1},
    70: {"key": "A#4", "servo": 16, "servo_direction": 0},

    73: {"key": "C#5", "servo": 17, "servo_direction": 0},
    75: {"key": "D#5", "servo": 17, "servo_direction": 1},
    78: {"key": "F#5", "servo": 18, "servo_direction": 0},
    80: {"key": "G#5", "servo": 18, "servo_direction": 1},
    82: {"key": "A#5", "servo": 19, "servo_direction": 0},
    85: {"key": "C#6", "servo": 19, "servo_direction": 1}
}
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_label.config(text=f"Selected Folder: {folder_path}")
        update_file_dropdown(folder_path)

def update_file_dropdown(folder_path):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".mid")]
    file_var.set("Select a file")
    file_menu['menu'].delete(0, 'end')
    for file in txt_files:
        file_menu['menu'].add_command(label=file, command=tk._setit(file_var, file))
    global selected_folder
    selected_folder = folder_path
    if txt_files:
        start_button.config(state=tk.NORMAL)

def start_playback():
    selected_file = os.path.join(selected_folder, file_var.get())
    if selected_file:
        play_notes_from_file(selected_file)

def calculate_delay(velocity):
    min_delay = 100
    max_delay = 500
    delay = (min_delay + (max_delay - min_delay) * (127 - velocity) / 127)
    return int(delay)
servo_state = {servo["servo"]: servo["servo_direction"] for servo in note_map.values()}

# Function to play MIDI file and send servo instructions
def play_notes_from_file(file_path):
    arduino = serial.Serial(port= 'COM9', baudrate=9600, timeout=.1)  # Replace
    midi_file = mido.MidiFile(file_path)
    time.sleep(2)

    for msg in midi_file.play():
        print(msg)
        if (msg.type == 'note_on' or msg.type == 'note_off'):#) and msg.channel == channel:
            note = msg.note
            velocity = msg.velocity
            #print(msg.note)

            if note in note_map:
                servo_no = note_map[note]["servo"]
                action = "1" if msg.type == 'note_on' else "0"
                servo_direction = note_map[note]["servo_direction"]

                if msg.type == 'note_off':
                    servo_direction = 1 - servo_direction  # Reverse direction for release
               
                output = f"{servo_no:02}{action}{servo_direction}{msg.time:.3f}\n"
                print(output)
                arduino.write(output.encode())
                response = arduino.readline().decode().strip()  # Read response
                print("from ard" + response)
                time.sleep(0.1)
    arduino.close();


root = tk.Tk()
root.title("MIDI File Player")
root.geometry("500x350")
root.configure(bg="#ecf0f1")

header_label = tk.Label(root, text="🎵 MIDI File Selector 🎵", font=("Arial", 16, "bold"), bg="#3498db", fg="white", padx=10, pady=5)
header_label.pack(fill=tk.X, pady=10)

file_label = tk.Label(root, text="No folder selected", font=("Arial", 10), bg="#ecf0f1", wraplength=400)
file_label.pack(pady=5)

select_folder_button = tk.Button(root, text="📂 Select Folder", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", width=20, relief=tk.GROOVE, command=select_folder)
select_folder_button.pack(pady=5)

file_var = tk.StringVar(root)
file_var.set("Select a file")
file_menu = tk.OptionMenu(root, file_var, "")
file_menu.config(font=("Arial", 10), width=20, bg="#f39c12", fg="white")
file_menu.pack(pady=5)

start_button = tk.Button(root, text="▶️ Start Playback", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", width=20, relief=tk.RAISED, state=tk.DISABLED, command=start_playback)
start_button.pack(pady=10)

selected_folder = None

root.mainloop()
