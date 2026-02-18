"""
Generate Figure for H5 Hypothesis Validation Example.

This figure shows the VOLTA pipeline with particle-based statistical independence.
Only shows Round 3 (Particle-Level Correlation Magnitude Consistency Test).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.image import imread
import numpy as np

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11

# Color scheme
COLORS = {
    'hypothesis': '#9B59B6',     # Purple
    'agent': '#4A90D9',          # Blue
    'tool': '#E67E22',           # Orange
    'code': '#2C3E50',           # Dark
    'result': '#5CB85C',         # Green
    'stats': '#F0AD4E',          # Orange
    'background': '#F8F9FA',
    'warning': '#E74C3C',        # Red
}


def create_h5_example_figure():
    """Create a figure showing the H5 validation process with particle identification."""

    fig = plt.figure(figsize=(14, 11))

    # Create grid layout - simplified: 3 rows, 2 columns in last row
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.25,
                          height_ratios=[0.7, 1.6, 0.8])

    # === Panel A: Hypothesis Input ===
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('(A) Hypothesis Input', fontweight='bold', loc='left')

    hypothesis_text = (
        "H5: The A1g peak position and\n"
        "ID/IG ratio show weak or no\n"
        "spatial correlation, indicating\n"
        "decoupled cathode-carbon behavior.\n"
        "Expected: |r| < 0.05"
    )

    box = FancyBboxPatch((0.3, 1.5), 9.4, 7,
                         boxstyle="round,pad=0.1,rounding_size=0.3",
                         facecolor='#E8E0F0', edgecolor=COLORS['hypothesis'],
                         linewidth=2)
    ax1.add_patch(box)
    ax1.text(5, 5, hypothesis_text, ha='center', va='center', fontsize=9,
             style='italic', wrap=True)

    # === Panel B: Test Proposal Agent Output ===
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('(B) Test Proposal Agent', fontweight='bold', loc='left')

    proposal_text = (
        "Particle-Level Correlation\n"
        "Magnitude Consistency Test\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "H₀: Mean |r| ≤ 0.05\n"
        "    (weak correlations)\n\n"
        "H₁: Mean |r| > 0.05\n"
        "    (strong correlations)\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Method: One-sample t-test\n"
        "on |r| per particle"
    )

    box = FancyBboxPatch((0.3, 0.3), 9.4, 9.4,
                         boxstyle="round,pad=0.1,rounding_size=0.3",
                         facecolor='#E3F2FD', edgecolor=COLORS['agent'],
                         linewidth=2)
    ax2.add_patch(box)
    ax2.text(5, 5, proposal_text, ha='center', va='center', fontsize=8,
             family='monospace')

    # === Panel C: Tool Call ===
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    ax3.set_title('(C) Particle Identification Tool', fontweight='bold', loc='left')

    tool_text = (
        "Action: identify_particles\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Input:\n"
        '  {"time_idx": 0,\n'
        '   "min_particle_size": 4,\n'
        '   "return_timeseries": true}\n'
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Output:\n"
        "  5 particles identified\n"
        "  → INDEPENDENT EVENTS"
    )

    box = FancyBboxPatch((0.3, 0.3), 9.4, 9.4,
                         boxstyle="round,pad=0.1,rounding_size=0.3",
                         facecolor='#FFF3E0', edgecolor=COLORS['tool'],
                         linewidth=2)
    ax3.add_patch(box)
    ax3.text(5, 5, tool_text, ha='center', va='center', fontsize=8,
             family='monospace')

    # === Panel D: Particle Identification Visualization (LARGER) ===
    ax4 = fig.add_subplot(gs[1, :])

    # Load the particle identification image
    try:
        img = imread('../paper/paper_figs/particle_identification.png')
        ax4.imshow(img)
        ax4.axis('off')
    except:
        # Fallback: create a simulated particle visualization
        ax4.set_xlim(0, 30)
        ax4.set_ylim(0, 30)
        ax4.text(15, 15, '[Particle Image]', ha='center', va='center', fontsize=14)
        ax4.set_aspect('equal')

    ax4.set_title('(D) Spatially Isolated Particles Identified from A1g Intensity (n=5 independent events)',
                  fontweight='bold', loc='left', fontsize=11)

    # === Panel E: Per-Particle Correlations ===
    ax5 = fig.add_subplot(gs[2, 0])

    # Actual correlation data from H5 test
    particles = ['P1', 'P2', 'P3', 'P4', 'P5']
    correlations = [0.714, -0.061, 0.510, 0.635, 0.478]
    abs_correlations = [abs(c) for c in correlations]

    colors = ['#E74C3C' if c > 0.05 else '#2ECC71' for c in abs_correlations]
    bars = ax5.barh(particles, abs_correlations, color=colors, edgecolor='black', linewidth=1)

    # Threshold line
    ax5.axvline(x=0.05, color='red', linestyle='--', linewidth=2, label='Threshold (0.05)')
    ax5.axvline(x=np.mean(abs_correlations), color='blue', linestyle='-', linewidth=2, label=f'Mean ({np.mean(abs_correlations):.3f})')

    ax5.set_xlabel('|r|')
    ax5.set_title('(E) Per-Particle |r|', fontweight='bold', loc='left')
    ax5.set_xlim(0, 0.8)
    ax5.legend(loc='lower right', fontsize=7)

    # === Panel F: Statistical Results & Validation Outcome (spans 2 columns) ===
    ax6 = fig.add_subplot(gs[2, 1:])
    ax6.set_xlim(0, 10)
    ax6.set_ylim(0, 10)
    ax6.axis('off')
    ax6.set_title('(F) Statistical Results & Validation Outcome', fontweight='bold', loc='left')

    # Results box
    box = FancyBboxPatch((0.3, 0.5), 9.4, 9,
                         boxstyle="round,pad=0.1,rounding_size=0.3",
                         facecolor='#FFEBEE', edgecolor=COLORS['warning'],
                         linewidth=2)
    ax6.add_patch(box)

    results_text = (
        "One-Sample t-Test (H₀: mean |r| ≤ 0.05)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "n = 5 particles    Mean |r| = 0.479\n"
        "t = 3.80           p = 9.55 × 10⁻³\n"
        "E-value = 104.7 > 10 (α = 0.1)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "VALIDATION COMPLETE\n"
        "Hypothesis H5: FALSIFIED\n"
        "(Strong correlations detected)"
    )
    ax6.text(5, 5, results_text, ha='center', va='center', fontsize=10,
             family='monospace', fontweight='bold')

    plt.suptitle('VOLTA Validation Pipeline: Hypothesis H5 (Cathode-Carbon Decoupling)\nParticle-Based Statistical Independence Test',
                 fontsize=13, fontweight='bold', y=0.99)

    plt.tight_layout()
    plt.savefig('figure8_h5_example.pdf', dpi=300, bbox_inches='tight')
    plt.savefig('figure8_h5_example.png', dpi=300, bbox_inches='tight')
    print("Saved figure8_h5_example.pdf and figure8_h5_example.png")
    plt.close()


if __name__ == "__main__":
    create_h5_example_figure()
