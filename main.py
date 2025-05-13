from core.eeg_processor import preprocess_eeg
from core.music_mapper import eeg_to_music_parameters
from core.midi_generator import json_to_midi
from core.midi_visualizer import visualize_midi
from visualization.plots import create_all_visualizations
from utils.cli import (
    Spinner, print_header, print_success, print_error, print_info,
    clear_screen, log_to_file
)
from utils.config import config
from pathlib import Path
import time


def setup_directories():
    """Create necessary output directories"""
    for path in config.get('paths', 'output').values():
        Path(path).mkdir(parents=True, exist_ok=True)


def handle_midi_visualization(midi_path: str):
    """Handle MIDI file visualization and analysis."""
    print(f"\nAnalyzing MIDI file: {midi_path}")

    stats = (midi_path)
    if stats:
        print("\nMIDI Analysis Results:")
        print(f"Total notes: {stats['total_notes']}")
        print(f"Unique notes: {stats['unique_notes']}")
        print(f"Duration: {stats['duration']} ticks")
        print("\nVisualizations saved to:")
        for name, path in stats['visualization_files'].items():
            print(f"- {name}: {path}")
    else:
        print("Failed to analyze MIDI file")


def main():
    clear_screen()
    print_header("EEG to Music Conversion Tool")
    print_info("Starting processing pipeline...")
    setup_directories()

    # Get paths from config
    output_paths = config.get('paths', 'output')

    # File paths
    eeg_file = Path('data/sample_data/EEG_wav.set')
    preprocessed_eeg_path = Path(output_paths['json']) / 'wave_analysis.json'
    eeg_music_params_path = Path(
        output_paths['json']) / 'music_parameters.json'
    eeg_global_music_params_path = Path(
        output_paths['json']) / 'global_parameters.json'

    spinner = Spinner()
    start_time = time.time()

    try:
        # Step 1: Preprocess EEG data
        print_header("Step 1: EEG Preprocessing")
        for _ in range(20):
            spinner.spin("Processing EEG data...")
            time.sleep(0.1)
        results = preprocess_eeg(eeg_file)
        print_success("EEG preprocessing completed successfully")
        log_to_file("EEG preprocessing completed")

        # Step 2: Generate music parameters
        print_header("Step 2: Music Parameter Generation")
        for _ in range(15):
            spinner.spin("Generating music parameters...")
            time.sleep(0.1)
        eeg_to_music_parameters(preprocessed_eeg_path)
        print_success("Music parameters generated successfully")
        log_to_file("Music parameters generated")

        # Step 3: Create MIDI file
        print_header("Step 3: MIDI File Creation")
        for _ in range(10):
            spinner.spin("Creating MIDI file...")
            time.sleep(0.1)
        json_to_midi(eeg_music_params_path)
        print_success("MIDI file created successfully")
        log_to_file("MIDI file created")

        # Step 4: Create MIDI visualization
        print_header("Step 4: MIDI Visualization")
        for _ in range(10):
            spinner.spin("Creating MIDI visualization...")
            time.sleep(0.1)
        csv_path, _ = visualize_midi(
            'output/midi/midi_out.mid', output_paths['json'])
        print_success("MIDI visualization created successfully")
        log_to_file("MIDI visualization created")

        # Step 5: Generate visualizations
        print_header("Step 5: Visualization Generation")
        for _ in range(25):
            spinner.spin("Generating visualizations...")
            time.sleep(0.1)
        create_all_visualizations(preprocessed_eeg_path, eeg_music_params_path)
        print_success("Visualizations generated successfully")
        log_to_file("Visualizations generated")
        
        # Final summary
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)

        print_header("Processing Summary")
        print_info(f"Total processing time: {processing_time} seconds\n")
        print_info("Generated files:")
        print("  └─ wave_analysis.json")
        print("  └─ music_parameters.json")
        print("  └─ midi_out.mid")
        print("  └─ output.mp3")
        print("  └─ midi_visualization.csv")
        print("  └─ analysis/")
        print("     ├─ wave_strengths_plot.png")
        print("     ├─ wave_distribution_boxplot.png")
        print("     ├─ wave_heatmap.png")
        print("     └─ music_parameters.png\n")

    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        log_to_file(f"Error: {str(e)}")
        return


if __name__ == "__main__":
    main()
