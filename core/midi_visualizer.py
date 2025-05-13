import py_midicsv as pm

def visualize_midi(midi_file_path: str, output_dir: str = None) -> tuple:
    """
    Convert MIDI file to CSV for visualization and analysis.
    
    Args:
        midi_file_path (str): Path to the MIDI file
        output_dir (str, optional): Directory to save CSV file. If None, uses same directory as MIDI.
    
    Returns:
        tuple: (csv_path, csv_content) - Path to saved CSV file and the CSV content as list
    """
    try:
        # Convert MIDI to CSV format
        csv_content = pm.midi_to_csv(midi_file_path)
        
        # Determine output path
        # midi_path = Path(midi_file_path)
        # if output_dir:
        #     output=_path = Path(output_dir) / f"{midi_path.stem}_visualization.csv"
        # else:
        #     output_path = midi_path.with_name(f"{midi_path.stem}_visualization.csv")
        
        output_path = 'output/midi/midi_visualization.csv'
        # Ensure output directory exists
        # os.makedirs(output_path.parent, exist_ok=True)
        
        # Save CSV file
        with open(output_path, "w") as f:
            f.writelines(csv_content)
            
        return str(output_path), csv_content
        
    except Exception as e:
        print(f"Error visualizing MIDI file: {str(e)}")
        return None, None