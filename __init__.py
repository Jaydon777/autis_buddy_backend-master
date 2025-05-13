"""
Autis Buddy
===========

A tool for converting EEG data to music for therapeutic purposes.

Main components:
- EEG Processing
- Music Parameter Mapping
- MIDI Generation
- Data Visualization
"""

__version__ = "0.1.0"
__author__ = "Aadityaa Nagarajan"
__description__ = "EEG to Music conversion tool for therapeutic purposes"

# Import key components for easy access
from core.eeg_processor import preprocess_eeg
from core.music_mapper import eeg_to_music_parameters
from core.midi_generator import json_to_midi
from visualization.plots import create_all_visualizations
from utils.config import config

# Define what should be available when using "from autis_buddy import *"
__all__ = [
    'preprocess_eeg',
    'eeg_to_music_parameters',
    'json_to_midi',
    'convert_midi_to_mp3'
    'create_all_visualizations',
    'config',

]
