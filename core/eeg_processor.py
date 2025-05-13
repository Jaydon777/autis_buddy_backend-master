import mne
import numpy as np
from scipy import signal
import json
import os
import warnings

# Suppress the specific RuntimeWarning
warnings.filterwarnings('ignore', category=RuntimeWarning, message='The data contains.*boundary.*events')


def preprocess_eeg(filename, interval_length=5):
    """
    Analyze EEG data to extract wave band strengths in specified time intervals.
    
    Parameters:
    filename (str): Path to the .set file
    interval_length (int): Length of each interval in seconds
    
    Returns:
    dict: Dictionary containing the analysis results
    """
    # Load the EEG data
    raw = mne.io.read_raw_eeglab(filename, preload=True)
    
    # Get sampling frequency and data
    sfreq = raw.info['sfreq']
    data = raw.get_data()
    
    # Calculate samples per interval
    samples_per_interval = int(interval_length * sfreq)
    
    # Calculate number of complete intervals
    total_samples = data.shape[1]
    num_intervals = total_samples // samples_per_interval
    
    # Define frequency bands
    freq_bands = {
        'delta': (0.5, 4),
        'theta': (4, 8),
        'alpha': (8, 13),
        'beta': (13, 30),
        'gamma': (30, min(sfreq/2, 100))  # Upper limit capped at Nyquist frequency or 100 Hz
    }
    
    # Initialize results dictionary
    results = {
        "interval_length": str(interval_length),
        "wave_strengths": {}
    }
    
    # Process each interval
    for interval in range(num_intervals):
        # Extract data for current interval
        start_idx = interval * samples_per_interval
        end_idx = (interval + 1) * samples_per_interval
        interval_data = data[:, start_idx:end_idx]
        
        # Calculate power spectrum using Welch's method
        freqs, psd = signal.welch(interval_data, fs=sfreq, nperseg=min(samples_per_interval, 256))
        psd = np.mean(psd, axis=0)  # Average across channels
        
        # Calculate power in each frequency band
        band_powers = []
        for band in freq_bands.values():
            freq_mask = (freqs >= band[0]) & (freqs <= band[1])
            band_power = np.sum(psd[freq_mask])
            band_powers.append(band_power)
        
        # Convert to percentages
        total_power = sum(band_powers)
        percentages = [power/total_power for power in band_powers]
        
        # Store results as strings
        results["wave_strengths"][str(interval + 1)] = [f"{p:.3f}" for p in percentages]
    
    # Save results to JSON file
    output_dir = 'output/json'
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, 'wave_analysis.json')
    
    with open(output_filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis complete. Results saved to: {output_filename}")
    return results

