from mido import Message, MidiFile, MidiTrack

# Define note-to-MIDI mapping
note_map = {
    "C3": 48, "C#3": 49, "D3": 50, "D#3": 51, "E3": 52, "F3": 53, "F#3": 54, "G3": 55, "G#3": 56, "A3": 57, "A#3": 58, "B3": 59,
    "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65, "F#4": 66, "G4": 67, "G#4": 68, "A4": 69, "A#4": 70, "B4": 71,
    "C5": 72
}


# Read note sequence from the text file
note_sequence = """
F4  F4  D4  F4  G4  A4   F4  F4  D4  A4  F4  F4  E4 E4  E4  D4  F4  F4  D4  F4  G4  A4 F4  F4  C4  A4  F4  G4  A4   A4  A4  G4  A4 A4  A4  G4  A4  F4  G4  G4  G4  A4  G4  F4  D4  A4  A4  A4  G4  F4  G4  G4  G4  A4  G4  F4  E4  F4  A4  A4  A4  G4  A4  F4  E4  D4  C5  C5  C5  A4  F4  C5  A4  A4  A4  A4  G4  A4  F4  E4  D4  B4  C5  A4  C5  A4  C5  A4  F4  B4  F4  B4  A4  F4  B4  A4  F4  E4  F4  B4  A4  F4  B4  A4  F4  E4  
"""

# Process note sequence and create MIDI file
midi = MidiFile()
track = MidiTrack()
midi.tracks.append(track)

# Convert note sequence to MIDI messages
for note in note_sequence.split():
    midi_note = note_map.get(note, None)
    if midi_note:
        track.append(Message('note_on', note=midi_note, velocity=64, time=120))
        track.append(Message('note_off', note=midi_note, velocity=64, time=120))

# Save MIDI file
midi_filename = "/Users/sudhanshukulkarni/projects/Auto_Orchestra/Faded.mid"
midi.save(midi_filename)
midi_filename
