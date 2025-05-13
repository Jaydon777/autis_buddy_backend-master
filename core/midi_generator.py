import json
from mido import Message, MidiFile, MidiTrack, MetaMessage

def json_to_midi(eeg_music_params_path: str, eeg_global_music_params_path: str):
    """
    Generate a MIDI file from EEG-derived musical parameters and global parameters
    
    Args:
        eeg_music_params_path: Path to the JSON file with note-level musical parameters
        eeg_global_music_params_path: Path to the JSON file with global musical parameters
    """
    # Load note parameters
    with open(eeg_music_params_path, 'r') as f:
        data = json.load(f)
        interval_length = int(data['interval_length'])
        musical_parameters = data['musical_parameters']
    
    # Load global parameters
    with open(eeg_global_music_params_path, 'r') as f:
        global_params = json.load(f)
        wave_strengths = global_params['average_wave_strengths']
        global_musical_params = global_params['musical_parameters']
    
    # Create MIDI file
    midi = MidiFile(type=1)  # Type 1 allows multiple tracks
    
    # Create a tempo track (track 0)
    tempo_track = MidiTrack()
    midi.tracks.append(tempo_track)
    
    # Set tempo based on global parameters
    tempo = global_musical_params['tempo']
    # MIDI tempo is in microseconds per quarter note
    tempo_in_microseconds = int(60000000 / tempo)
    tempo_track.append(MetaMessage('set_tempo', tempo=tempo_in_microseconds, time=0))
    
    # Set time signature (4/4 by default)
    tempo_track.append(MetaMessage('time_signature', numerator=4, denominator=4, 
                                   clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    
    # Add a text marker for the key instead of using key_signature
    key = global_musical_params['key']
    tempo_track.append(MetaMessage('text', text=f"Key: {key}", time=0))
    
    # Create a track for the notes
    note_track = MidiTrack()
    midi.tracks.append(note_track)
    
    # Optional: Add a track name
    note_track.append(MetaMessage('track_name', name='EEG-Generated Notes', time=0))
    
    # Add instrument selection (default to piano)
    note_track.append(Message('program_change', program=0, time=0))  # 0 = Acoustic Grand Piano
    
    # Calculate dynamic range adjustment based on wave strengths if needed
    # For example, more beta/gamma activity could increase dynamics
    dynamic_factor = 1.0 + (wave_strengths['beta'] + wave_strengths['gamma']) / 2
    
    # Add notes to track
    for key, params in musical_parameters.items():
        note = int(params[0])
        duration = float(params[1])
        velocity = int(float(params[2]) * 127 * dynamic_factor)  # Apply dynamic factor
        
        # Clamp velocity to valid MIDI range (0-127)
        velocity = max(0, min(127, velocity))
        
        # Add note events
        note_track.append(Message('note_on', note=note, velocity=velocity, time=0))
        note_track.append(Message('note_off', note=note, velocity=velocity, 
                                  time=int(duration * 480)))  # 480 ticks per beat
    
    # Save the MIDI file
    output_file = 'output/midi/midi_out.mid'
    midi.save(output_file)
    
    return output_file