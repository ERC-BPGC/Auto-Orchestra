import tkinter as tk
from tkinter import filedialog
import serial
import time
import os

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
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_label.config(text=f"Selected Folder: {folder_path}")
        update_file_dropdown(folder_path)

def update_file_dropdown(folder_path):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
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

def play_notes_from_file(file_path):
    arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
    
    with open(file_path, 'r') as file:
        for line in file:
            notes = line.strip().split(', ')
            for note_group in notes:
                for note in note_group.split():
                    if note in note_map:
                        servo_no = note_map[note]["keyboard_servo"]
                        servo_direction = note_map[note]["keyboard_direction"]

                        delay = calculate_delay(100)  
                        output = f"{servo_no:02}{delay:04}{servo_direction}"
                        print(f"Note {note} pressed: Output Code = {output}")
                        arduino.write((output + "\n").encode())
                        time.sleep(delay / 1000.0)
                
                time.sleep(0.1)
    
    arduino.close()

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

start_button = tk.Button(root, text="▶ Start Playback", font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", width=20, relief=tk.RAISED, state=tk.DISABLED, command=start_playback)
start_button.pack(pady=10)

selected_folder = None  

root.mainloop()