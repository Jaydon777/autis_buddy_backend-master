# Autis Buddy

A sophisticated tool for converting EEG (Electroencephalogram) data into musical compositions, specifically designed for therapeutic purposes in autism treatment.

## Overview

Autis Buddy processes raw EEG data through multiple stages to create meaningful musical output that corresponds to brain wave patterns. This creates an auditory representation of neural activity that can be used for therapeutic purposes.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/autis_buddy.git
cd autis_buddy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
autis_buddy/
├── core/           # Core processing modules
│   ├── eeg_processor.py    # EEG data analysis
│   ├── music_mapper.py     # EEG to music conversion
│   └── midi_generator.py   # MIDI file generation
├── visualization/  # Visualization tools
│   └── plots.py            # Data plotting functions
├── utils/         # Utility functions
│   ├── cli.py             # CLI interface
│   └── config.py          # Configuration handler
├── data/          # Sample data
└── config/        # Configuration files
```

## How It Works

### 1. EEG Processing
- Reads raw EEG data from .set files
- Performs frequency band analysis (Delta, Theta, Alpha, Beta, Gamma)
- Calculates wave strength percentages for each time interval
- Outputs processed data in JSON format

### 2. Music Parameter Mapping
- Converts EEG wave strengths into musical parameters:
  - Delta waves → Base pitch
  - Gamma waves → Pitch variation
  - Beta waves → Step intervals
  - Delta/Beta combination → Note duration

### 3. MIDI Generation
- Creates MIDI files based on the calculated musical parameters
- Generates continuous musical sequences
- Maintains musical coherence while representing EEG patterns

## Visualizations

The tool generates several visualizations to help understand the EEG-to-music conversion process:

### Wave Strength Distribution
![Wave Distribution Boxplot](screenshots/wave_distribution_boxplot.png)
*Distribution of different wave types across the recording*

### Wave Strength Heatmap
![Wave Heatmap](screenshots/wave_heatmap.png)
*Temporal visualization of wave strength variations*

### Music Parameters
![Music Parameters](screenshots/music_parameters.png)
*Generated musical parameters over time*

## Configuration

The tool can be configured through `config/config.yaml`:

```yaml
paths:
  output:
    midi: output/midi
    json: output/json
    plots: output/plots
  data: data/sample_data

processing:
  eeg:
    interval_length: 5
    frequency_bands:
      delta: [0.5, 4]
      theta: [4, 8]
      alpha: [8, 13]
      beta: [13, 30]
      gamma: [30, 100]

visualization:
  plot_settings:
    figsize: [12, 6]
    dpi: 100
    style: default
```

## Usage

1. Basic usage:
```bash
python main.py
```

2. The tool will:
   - Process input EEG data
   - Generate visualizations
   - Create MIDI output
   - Save analysis results

## Output Files

The tool generates several output files:
- `wave_analysis.json`: Processed EEG data
- `music_parameters.json`: Generated musical parameters
- `midi_out.mid`: Final musical composition
- Various visualization plots in the `output/plots` directory

## MIDI Generation Formulas

The MIDI generation process uses specific formulas to convert EEG data into musical parameters:

1. **Velocity Calculation**: 
   ```
   MIDI_velocity = EEG_amplitude * 127
   ```
   - Converts normalized EEG amplitude (0-1) to MIDI velocity range (0-127)
   - Higher amplitudes result in louder notes
   - Used to represent the intensity of brain activity

2. **Time Calculation**: 
   ```
   MIDI_ticks = duration * 480
   ```
   - Converts duration in seconds to MIDI ticks
   - Uses 480 ticks per beat (standard MIDI resolution)
   - Ensures accurate timing representation

These formulas maintain the relationship between:
- EEG signal strength → Note velocity (loudness)
- Time intervals → Note duration
This creates a direct mapping between brain activity and musical expression.

## Contributing

Contributions are welcome! Please drop a mail at aadityaa2606@gmail.com