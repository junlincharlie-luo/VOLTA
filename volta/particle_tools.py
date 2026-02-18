import numpy as np
import pandas as pd
from scipy import ndimage
from scipy.ndimage import label, gaussian_filter
from langchain.tools import BaseTool
from pydantic import PrivateAttr
from typing import Dict, Optional
import matplotlib.pyplot as plt


class ParticleIdentifier:
    """Identifies isolated particles from A1g spatial intensity data."""

    def __init__(self, df_raman_peaks: pd.DataFrame):
        self.df = df_raman_peaks
        self.grid_size = 30

    def get_heatmap(self, time_idx: int, column: str = 'A1g_Amp') -> np.ndarray:
        """Extract 30x30 heatmap for given time and column."""
        data = self.df[self.df['time_idx'] == time_idx]
        heatmap = np.zeros((self.grid_size, self.grid_size))
        for _, row in data.iterrows():
            heatmap[int(row['Y']), int(row['X'])] = row[column]
        return heatmap

    def identify_particles(self, time_idx: int = 0,
                          intensity_column: str = 'A1g_Amp',
                          threshold_method: str = 'adaptive',
                          min_particle_size: int = 4,
                          smoothing_sigma: float = 1.0) -> dict:
        """
        Segment particles based on intensity threshold and connectivity.

        Returns dict with:
        - 'labels': 30x30 array with particle IDs (0=background)
        - 'n_particles': number of particles found
        - 'particle_stats': DataFrame with per-particle statistics
        - 'particle_pixels': dict mapping particle_id to list of (x,y) coords
        """
        # Get intensity heatmap
        heatmap = self.get_heatmap(time_idx, intensity_column)

        # Smooth to reduce noise
        smoothed = gaussian_filter(heatmap, sigma=smoothing_sigma)

        # Threshold to identify active regions
        if threshold_method == 'adaptive':
            threshold = np.mean(smoothed) + 0.5 * np.std(smoothed)
        else:
            threshold = np.percentile(smoothed, 75)

        binary = smoothed > threshold

        # Connected component labeling (8-connectivity)
        structure = np.ones((3, 3))  # 8-connectivity
        labels, n_features = label(binary, structure=structure)

        # Filter small components
        particle_stats = []
        valid_labels = np.zeros_like(labels)
        particle_pixels = {}
        new_id = 0

        for i in range(1, n_features + 1):
            mask = labels == i
            size = np.sum(mask)
            if size >= min_particle_size:
                new_id += 1
                valid_labels[mask] = new_id

                # Get pixel coordinates
                coords = np.where(mask)
                particle_pixels[new_id] = list(zip(coords[1], coords[0]))  # (x, y)

                # Calculate statistics
                particle_stats.append({
                    'particle_id': new_id,
                    'size_pixels': size,
                    'centroid_x': np.mean(coords[1]),
                    'centroid_y': np.mean(coords[0]),
                    'mean_intensity': np.mean(heatmap[mask]),
                    'max_intensity': np.max(heatmap[mask])
                })

        return {
            'labels': valid_labels,
            'n_particles': new_id,
            'particle_stats': pd.DataFrame(particle_stats),
            'particle_pixels': particle_pixels,
            'time_idx': time_idx
        }

    def get_particle_timeseries(self, particle_pixels: dict,
                                column: str = 'A1g_Center') -> pd.DataFrame:
        """
        Extract timeseries of a column for each particle.

        Returns DataFrame with columns: time_idx, particle_id, mean_value, std_value
        """
        results = []
        time_indices = self.df['time_idx'].unique()

        for time_idx in sorted(time_indices):
            time_data = self.df[self.df['time_idx'] == time_idx]

            for pid, pixels in particle_pixels.items():
                values = []
                for x, y in pixels:
                    pixel_data = time_data[(time_data['X'] == x) & (time_data['Y'] == y)]
                    if len(pixel_data) > 0:
                        values.append(pixel_data[column].values[0])

                if values:
                    results.append({
                        'time_idx': time_idx,
                        'particle_id': pid,
                        'mean_value': np.mean(values),
                        'std_value': np.std(values),
                        'n_pixels': len(values)
                    })

        return pd.DataFrame(results)

    def visualize_particles(self, result: dict, save_path: str = None):
        """Plot identified particles on heatmap."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Original intensity
        heatmap = self.get_heatmap(result['time_idx'], 'A1g_Amp')
        im1 = axes[0].imshow(heatmap, cmap='hot', origin='lower')
        axes[0].set_title(f'A1g Amplitude (time_idx={result["time_idx"]})')
        plt.colorbar(im1, ax=axes[0])

        # Particle labels
        im2 = axes[1].imshow(result['labels'], cmap='tab20', origin='lower')
        axes[1].set_title(f'Identified Particles (n={result["n_particles"]})')
        plt.colorbar(im2, ax=axes[1])

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()
        return fig


class ParticleIdentificationTool(BaseTool):
    """LangChain tool for particle identification."""

    name: str = "identify_particles"
    description: str = """
Identifies spatially isolated particles from A1g peak intensity data.
Use this tool to get independent events for statistical testing instead of using the 900 correlated pixels.

Input format (as Python dict string):
{
    "time_idx": 0,  # Which time step to analyze (0-113)
    "min_particle_size": 4,  # Minimum pixels per particle
    "return_timeseries": true,  # Whether to compute particle timeseries
    "column": "A1g_Center"  # Column for timeseries (if requested)
}

Returns:
- Number of identified particles (typically 5-20)
- Particle statistics (size, centroid, intensity)
- Per-particle timeseries if requested (for correlation analysis)

Example usage:
Action: identify_particles
Action Input: {"time_idx": 0, "min_particle_size": 4, "return_timeseries": true, "column": "A1g_Center"}
"""

    _identifier: ParticleIdentifier = PrivateAttr()
    _last_result: dict = PrivateAttr(default=None)
    _exec_globals: Dict = PrivateAttr(default_factory=dict)

    def set_data(self, df_raman_peaks: pd.DataFrame):
        """Initialize with Raman data."""
        self._identifier = ParticleIdentifier(df_raman_peaks)

    def set_globals(self, exec_globals: Dict):
        """Set the shared globals namespace for variable sharing."""
        self._exec_globals = exec_globals

    def _run(self, query: str) -> str:
        """Execute particle identification."""
        import json
        try:
            # Parse input
            params = json.loads(query.replace("'", '"'))
            time_idx = params.get('time_idx', 0)
            min_size = params.get('min_particle_size', 4)
            return_ts = params.get('return_timeseries', False)
            column = params.get('column', 'A1g_Center')

            # Identify particles
            result = self._identifier.identify_particles(
                time_idx=time_idx,
                min_particle_size=min_size
            )
            self._last_result = result

            output = f"""
Particle Identification Results (time_idx={time_idx}):
- Number of particles identified: {result['n_particles']}
- These {result['n_particles']} particles can be treated as INDEPENDENT EVENTS for statistical testing

Particle Statistics:
{result['particle_stats'].to_string()}
"""

            if return_ts and result['n_particles'] > 0:
                ts = self._identifier.get_particle_timeseries(
                    result['particle_pixels'],
                    column=column
                )
                # Store in globals for agent to access
                output += f"""
Per-particle timeseries computed for '{column}'.
The timeseries DataFrame is stored as 'particle_timeseries' in your namespace.
Use this for per-particle correlation analysis with voltage.
"""
                # Make timeseries available
                self._exec_globals['particle_timeseries'] = ts
                self._exec_globals['particle_labels'] = result['labels']
                self._exec_globals['n_particles'] = result['n_particles']

            return output

        except Exception as e:
            return f"Error in particle identification: {str(e)}"

    async def _arun(self, query: str) -> str:
        return self._run(query)
