"""
Core Package
===========

Contains the main processing components for EEG analysis and music generation.
"""

from core.eeg_processor import preprocess_eeg
from core.music_mapper import eeg_to_music_parameters
from core.midi_generator import json_to_midi
from core.midi_visualizer import visualize_midi

__all__ = [
    'preprocess_eeg',
    'eeg_to_music_parameters',
    'json_to_midi',
    'visualize_midi',
    'convert_midi_to_mp3',
    'SUPPORTED_FORMATS',
    'SUPPORTED_OUTPUTS',
    'process_eeg_pipeline'
]

# Version of the core processing modules
__core_version__ = "0.1.0"

# Define the supported EEG file formats
SUPPORTED_FORMATS = ['.set', '.edf', '.bdf']

# Define the supported output formats
SUPPORTED_OUTPUTS = ['midi', 'json', 'mp3']

# Define a complete processing pipeline function
def process_eeg_pipeline(eeg_file_path, output_directory=None):
    """
    Run the complete EEG to music processing pipeline
    
    Args:
        eeg_file_path (str or Path): Path to the EEG file
        output_directory (str or Path, optional): Directory for output files
        
    Returns:
        dict: Dictionary with paths to all output files
    """
    from pathlib import Path
    from utils.config import config
    
    # Use default output paths from config if not specified
    if not output_directory:
        output_paths = config.get('paths', 'output')
    else:
        # Create a custom output structure
        output_directory = Path(output_directory)
        output_paths = {
            'json': str(output_directory / 'json'),
            'midi': str(output_directory / 'midi'),
            'visualization': str(output_directory / 'visualization')
        }
    
    # Create output directories if they don't exist
    for path in output_paths.values():
        Path(path).mkdir(parents=True, exist_ok=True)
    
    # Step 1: Preprocess EEG data
    preprocessed_eeg_path = Path(output_paths['json']) / 'wave_analysis.json'
    preprocess_eeg(eeg_file_path)
    
    # Step 2: Generate music parameters
    eeg_music_params_path = Path(output_paths['json']) / 'music_parameters.json'
    eeg_to_music_parameters(preprocessed_eeg_path)
    
    # Step 3: Create MIDI file
    midi_path = Path(output_paths['midi']) / 'midi_out.mid'
    json_to_midi(eeg_music_params_path)
    
    # Step 4: Create MIDI visualization
    csv_path, _ = visualize_midi(str(midi_path), output_paths['json'])
    
    # Step 5: Convert MIDI to MP3
    mp3_path = Path(output_paths['midi']) / 'output.mp3'
    convert_midi_to_mp3(str(midi_path), str(mp3_path))
    
    # Return paths to all generated files
    return {
        'preprocessed_eeg': str(preprocessed_eeg_path),
        'music_parameters': str(eeg_music_params_path),
        'midi_file': str(midi_path),
        'mp3_file': str(mp3_path),
        'midi_visualization': str(csv_path),
        'visualizations_dir': output_paths['visualization']
    }
