"""
Data Package
===========

Handles data loading, sample data management, and data validation.

Components:
- Data loading utilities
- Sample data access
- Data validation tools
"""

from pathlib import Path
from utils.config import config
import os

__all__ = [
    'get_sample_data_path',
    'list_sample_files',
    'validate_eeg_file'
]

def get_sample_data_path() -> Path:
    """Returns the path to sample data directory"""
    base_path = Path(__file__).parent.parent.parent
    return base_path / config.get('paths', 'data')

def list_sample_files(extension: str = None) -> list:
    """
    List available sample files.
    
    Args:
        extension (str, optional): Filter files by extension (e.g., '.set')
    
    Returns:
        list: List of available sample files
    """
    sample_path = get_sample_data_path()
    if extension:
        return [f for f in os.listdir(sample_path) if f.endswith(extension)]
    return os.listdir(sample_path)

def validate_eeg_file(filepath: Path) -> bool:
    """
    Validate if the given file is a valid EEG data file.
    
    Args:
        filepath (Path): Path to the EEG file
    
    Returns:
        bool: True if file is valid, False otherwise
    """
    if not filepath.exists():
        return False
    
    # Add more validation logic here as needed
    valid_extensions = ['.set', '.edf', '.bdf']
    
    # Basic validation - check file extension
    if filepath.suffix.lower() not in valid_extensions:
        return False
    
    # Check file size (avoid empty files)
    if filepath.stat().st_size < 100:  # Arbitrary minimum size
        return False
        
    # For more thorough validation, you could try to open the file
    # with appropriate libraries based on the file type
    
    return True
