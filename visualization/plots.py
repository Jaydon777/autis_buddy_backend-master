import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from pathlib import Path

def load_json_data(file_path):
    """Helper function to load JSON data"""
    with open(file_path, 'r') as f:
        return json.load(f)

def plot_wave_strengths(results):
    """
    Plot the wave strength percentages over time intervals.
    
    Parameters:
    results (dict): Analysis results from analyze_eeg_waves
    """
    
    # Convert data for plotting
    intervals = list(results["wave_strengths"].keys())
    wave_types = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    
    # Create matrix of values
    values = np.array([[float(v) for v in results["wave_strengths"][i]] 
                      for i in intervals])
    
    # Create plot
    plt.figure(figsize=(12, 6))
    for i in range(len(wave_types)):
        plt.plot(range(1, len(intervals) + 1), values[:, i], 
                label=wave_types[i], marker='o')
    
    plt.xlabel('Interval Number')
    plt.ylabel('Wave Strength (%)')
    plt.title('EEG Wave Strengths Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig('output/plots/wave_strengths_plot.png')

def plot_wave_distribution_boxplot(eeg_file):
    """Create a boxplot showing the distribution of each wave type"""
    data = load_json_data(eeg_file)
    wave_types = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    
    # Convert data to array
    values = []
    for wave_idx in range(5):
        wave_values = [float(data["wave_strengths"][interval][wave_idx]) 
                      for interval in data["wave_strengths"]]
        values.append(wave_values)

    plt.figure(figsize=(10, 6))
    plt.boxplot(values, labels=wave_types)
    plt.title('Distribution of Wave Strengths')
    plt.ylabel('Strength (%)')
    plt.grid(True, alpha=0.3)
    plt.savefig('output/plots/wave_distribution_boxplot.png')
    plt.close()

def plot_wave_heatmap(eeg_file):
    """Create a heatmap showing wave strengths over time"""
    data = load_json_data(eeg_file)
    wave_types = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    
    # Convert data to matrix
    values = np.array([[float(v) for v in data["wave_strengths"][str(i)]] 
                      for i in range(1, len(data["wave_strengths"]) + 1)])

    plt.figure(figsize=(12, 8))
    sns.heatmap(values.T, yticklabels=wave_types, cmap='viridis')
    plt.title('Wave Strength Heatmap Over Time')
    plt.xlabel('Time Interval')
    plt.ylabel('Wave Type')
    plt.savefig('output/plots/wave_heatmap.png')
    plt.close()

def plot_music_parameters(music_file):
    """Plot the generated music parameters"""
    data = load_json_data(music_file)
    intervals = list(data["musical_parameters"].keys())
    
    # Extract parameters
    pitch = [float(data["musical_parameters"][i][0]) for i in intervals]
    step = [float(data["musical_parameters"][i][1]) for i in intervals]
    duration = [float(data["musical_parameters"][i][2]) for i in intervals]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # Plot pitch
    ax1.plot(intervals, pitch, 'b-o')
    ax1.set_title('MIDI Pitch Over Time')
    ax1.set_ylabel('Pitch')
    ax1.grid(True)

    # Plot step
    ax2.plot(intervals, step, 'r-o')
    ax2.set_title('Step Intervals Over Time')
    ax2.set_ylabel('Step')
    ax2.grid(True)

    # Plot duration
    ax3.plot(intervals, duration, 'g-o')
    ax3.set_title('Note Duration Over Time')
    ax3.set_xlabel('Interval')
    ax3.set_ylabel('Duration')
    ax3.grid(True)

    plt.tight_layout()
    plt.savefig('output/plots/music_parameters.png')
    plt.close()

def plot_global_parameters(global_file):
    """Plot the global music parameters and average wave strengths"""
    data = load_json_data(global_file)
    
    # Create a figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Average Wave Strengths
    wave_types = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    wave_values = [data["average_wave_strengths"]["delta"], 
                   data["average_wave_strengths"]["theta"],
                   data["average_wave_strengths"]["alpha"],
                   data["average_wave_strengths"]["beta"],
                   data["average_wave_strengths"]["gamma"]]
    
    # Create bar chart
    bars = ax1.bar(wave_types, wave_values, color=['blue', 'green', 'red', 'purple', 'orange'])
    ax1.set_title('Average Wave Strengths')
    ax1.set_ylabel('Strength (%)')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    # Plot 2: Global Musical Parameters
    ax2.text(0.5, 0.7, f"Tempo: {data['musical_parameters']['tempo']} BPM", 
             fontsize=14, ha='center')
    ax2.text(0.5, 0.3, f"Key: {data['musical_parameters']['key']}", 
             fontsize=14, ha='center')
    ax2.axis('off')  # Hide axes
    ax2.set_title('Global Musical Parameters')
    
    plt.tight_layout()
    plt.savefig('output/plots/global_parameters.png')
    plt.close()

def create_all_visualizations(eeg_file, music_file):
    """Generate all visualizations"""
    # Create analysis directory if it doesn't exist
    Path('output/plots').mkdir(exist_ok=True)
    
    # Generate all plots
    plot_wave_distribution_boxplot(eeg_file)
    print("Wave distribution boxplot generated")
    plot_wave_heatmap(eeg_file)
    print("Wave heatmap generated")
    plot_music_parameters(music_file)
    print("Music parameters plot generated")
    
    # Add global parameters visualization
    global_file = "output/json/global_parameters.json"
    if os.path.exists(global_file):
        plot_global_parameters(global_file)
        print("Global parameters plot generated")
    
    print("All visualizations have been generated in the 'output/plots' directory")

if __name__ == "__main__":
    eeg_file = "output/json/wave_analysis.json"
    music_file = "output/json/music_parameters.json"
    create_all_visualizations(eeg_file, music_file)