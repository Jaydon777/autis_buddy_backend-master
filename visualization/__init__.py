"""
Visualization Package
===================

Provides visualization tools for EEG data and music parameters analysis.

Components:
- Wave strength plots
- Distribution analysis
- Heatmaps
- Music parameter visualizations
"""

__all__ = [
    'plot_wave_strengths',
    'plot_wave_distribution_boxplot',
    'plot_wave_heatmap',
    'plot_music_parameters',
    'create_all_visualizations'
]

from visualization.plots import (
    plot_wave_strengths,
    plot_wave_distribution_boxplot,
    plot_wave_heatmap,
    plot_music_parameters,
    create_all_visualizations
)
