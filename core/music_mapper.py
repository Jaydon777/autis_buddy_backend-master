import json
import numpy as np
import os
from pathlib import Path

def calculate_global_parameters(input_file):
    """
    Calculate global music parameters based on average EEG wave strengths.
    
    Parameters:
    input_file (str): Path to input JSON file containing EEG data
    
    Returns:
    dict: The global music parameters
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the input JSON file
    with open(input_file, 'r') as f:
        eeg_data = json.load(f)
    
    # Calculate average wave strengths
    wave_strengths = eeg_data["wave_strengths"]
    num_intervals = len(wave_strengths)
    
    # Initialize averages
    avg_delta = 0
    avg_theta = 0
    avg_alpha = 0
    avg_beta = 0
    avg_gamma = 0
    
    # Sum up all values
    for interval, strengths in wave_strengths.items():
        avg_delta += float(strengths[0])
        avg_theta += float(strengths[1])
        avg_alpha += float(strengths[2])
        avg_beta += float(strengths[3])
        avg_gamma += float(strengths[4])
    
    # Calculate averages
    avg_delta /= num_intervals
    avg_theta /= num_intervals
    avg_alpha /= num_intervals
    avg_beta /= num_intervals
    avg_gamma /= num_intervals
    
    # Calculate tempo
    tempo = 80 - 20 * (avg_beta + avg_gamma) / (avg_alpha + avg_theta + avg_delta + 0.01)
    tempo = round(tempo)  # Round to nearest integer
    
    # Ensure tempo is in range 60-80 bpm
    tempo = max(60, min(tempo, 80))
    
    # Determine key
    if avg_delta > avg_theta and avg_delta > avg_alpha and avg_delta > avg_beta and avg_delta > avg_gamma:
        key = "A minor"
    elif avg_theta > avg_alpha and avg_theta > avg_beta and avg_theta > avg_gamma:
        key = "C major"
    elif avg_alpha > avg_beta and avg_alpha > avg_gamma:
        key = "G major"
    else:  # beta or gamma is highest
        key = "A minor"
    
    # Create global parameters dictionary
    global_params = {
        "average_wave_strengths": {
            "delta": round(avg_delta, 3),
            "theta": round(avg_theta, 3),
            "alpha": round(avg_alpha, 3),
            "beta": round(avg_beta, 3),
            "gamma": round(avg_gamma, 3)
        },
        "musical_parameters": {
            "tempo": tempo,
            "key": key
        }
    }
    
    # Create output directory if it doesn't exist
    output_dir = Path('output/json')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to output JSON file
    output_file = 'output/json/global_parameters.json'
    with open(output_file, 'w') as f:
        json.dump(global_params, f, indent=2)
    
    print(f"Global parameters calculated and saved to: {output_file}")
    return global_params

def eeg_to_music_parameters(input_file):
    """
    Convert EEG wave strengths to musical parameters.

    Parameters:
    input_file (str): Path to input JSON file containing EEG data
    
    Returns:
    dict: The generated music parameters
    
    Raises:
    FileNotFoundError: If the input file doesn't exist
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the input JSON file
    with open(input_file, 'r') as f:
        eeg_data = json.load(f)

    # Initialize output dictionary
    music_data = {
        "interval_length": eeg_data["interval_length"],
        "musical_parameters": {}
    }

    # Process each interval
    for interval, wave_strengths in eeg_data["wave_strengths"].items():
        # Convert string percentages to float
        delta = float(wave_strengths[0])
        theta = float(wave_strengths[1])
        alpha = float(wave_strengths[2])
        beta = float(wave_strengths[3])
        gamma = float(wave_strengths[4])

        # Calculate musical parameters

        # Pitch (MIDI number)
        pitch = 60 + (delta * -10) + (gamma * 10) 
        pitch = round(np.clip(pitch, 0, 127))

        # Step (intervals)
        step = 2 + (beta * 5)
        step = round(step, 1)

        # Duration
        duration = 0.5 + (delta * 0.1) - (beta * 0.3)
        duration = round(max(0.1, duration), 2) 

        # Store the results
        music_data["musical_parameters"][interval] = [
            str(pitch),
            str(step),
            str(duration)
        ]

    # Create output directory if it doesn't exist
    output_dir = Path('output/json')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output filename based on input filename
    output_file = 'output/json/music_parameters.json'

    # Save to output JSON file
    with open(output_file, 'w') as f:
        json.dump(music_data, f, indent=2)
        
    # Calculate and save global parameters
    calculate_global_parameters(input_file)

    print(f"Conversion complete. Music parameters saved to: {output_file}")
    return music_data
