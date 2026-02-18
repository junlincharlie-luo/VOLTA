"""
Generate updated Figure 6 with Step 4 statistical test table.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

# Color scheme
COLORS = {
    'llm_agent': '#4A90D9',
    'statistical': '#5CB85C',
    'decision': '#F0AD4E',
    'human': '#D9534F',
    'data': '#9B59B6',
    'light_blue': '#E3F2FD',
    'light_green': '#E8F5E9',
    'light_orange': '#FFF3E0',
}


def create_figure_6_benchmark_results():
    """
    Figure 6: Benchmark Results with Step 4 Statistical Test Table.
    """
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.3, wspace=0.25)

    # === Panel A: Accuracy by domain ===
    ax1 = fig.add_subplot(gs[0, 0])
    domains = ['Biology', 'Economics', 'Sociology', 'Chemistry', 'Psychology', 'Physics']
    volta_acc = [0.90, 0.85, 0.82, 0.88, 0.80, 0.86]
    baseline_codegen = [0.70, 0.65, 0.60, 0.72, 0.62, 0.68]
    baseline_react = [0.75, 0.72, 0.68, 0.75, 0.70, 0.73]

    x = np.arange(len(domains))
    width = 0.25

    bars1 = ax1.bar(x - width, volta_acc, width, label='VOLTA', color=COLORS['llm_agent'], alpha=0.9)
    bars2 = ax1.bar(x, baseline_react, width, label='ReAct Baseline', color=COLORS['decision'], alpha=0.9)
    bars3 = ax1.bar(x + width, baseline_codegen, width, label='CodeGen Baseline', color=COLORS['human'], alpha=0.9)

    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.set_title('(A) Hypothesis Validation Accuracy by Domain', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(domains, rotation=15, ha='right')
    ax1.legend(loc='lower right', fontsize=9)
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3, axis='y')

    # === Panel B: Overall metrics comparison ===
    ax2 = fig.add_subplot(gs[0, 1])
    metrics = ['Accuracy', 'Type-I\nError', 'Power', 'Avg.\nTests']

    volta_norm = [0.90, 0.08, 0.85, 0.64]
    react_norm = [0.72, 0.15, 0.70, 0.90]
    codegen_norm = [0.65, 0.18, 0.62, 1.0]

    x2 = np.arange(len(metrics))

    bars4 = ax2.bar(x2 - width, volta_norm, width, label='VOLTA', color=COLORS['llm_agent'], alpha=0.9)
    bars5 = ax2.bar(x2, react_norm, width, label='ReAct Baseline', color=COLORS['decision'], alpha=0.9)
    bars6 = ax2.bar(x2 + width, codegen_norm, width, label='CodeGen Baseline', color=COLORS['human'], alpha=0.9)

    ax2.set_ylabel('Score (normalized)', fontsize=12)
    ax2.set_title('(B) Overall Performance Comparison', fontsize=12, fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(metrics)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_ylim(0, 1.2)
    ax2.grid(True, alpha=0.3, axis='y')

    ax2.axhline(y=0.1, color='green', linestyle='--', linewidth=1, alpha=0.7)
    ax2.text(1.3, 0.12, 'Target alpha=0.1', fontsize=8, color='green')

    summary_text = "VOLTA achieves 9/10 correct\nvalidations on verifiable hypotheses"
    ax2.text(0.5, 1.1, summary_text, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor=COLORS['light_green'], alpha=0.8))

    # === Panel C: Step 4 Statistical Test Table (H5 Example) ===
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    ax3.set_title('(C) Step 4: Statistical Test Results (H5 Particle Analysis)', fontsize=12, fontweight='bold')

    table_data = [
        ['Particle', 'Correlation (r)', '|r|'],
        ['1', '0.714', '0.714'],
        ['2', '−0.061', '0.061'],
        ['3', '0.510', '0.510'],
        ['4', '0.635', '0.635'],
        ['5', '0.478', '0.478'],
        ['Mean', '0.455', '0.479'],
    ]

    table = ax3.table(cellText=table_data[1:], colLabels=table_data[0],
                      loc='center', cellLoc='center',
                      colWidths=[0.25, 0.35, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2.0)

    for i in range(3):
        table[(0, i)].set_facecolor(COLORS['llm_agent'])
        table[(0, i)].set_text_props(color='white', fontweight='bold')

    for i in range(1, 7):
        abs_r = float(table_data[i][2])
        if abs_r > 0.05:
            table[(i, 2)].set_facecolor('#FFCDD2')
        else:
            table[(i, 2)].set_facecolor('#C8E6C9')
        if i % 2 == 0:
            table[(i, 0)].set_facecolor('#F5F5F5')
            table[(i, 1)].set_facecolor('#F5F5F5')
        if i == 6:
            for j in range(3):
                table[(i, j)].set_text_props(fontweight='bold')
                table[(i, j)].set_facecolor('#E3F2FD')

    ax3.text(0.5, 0.08, 'One-sample t-test: t = 3.80, p = 9.55 × 10⁻³\n'
             'Threshold = 0.05 | 4/5 particles exceed threshold\n'
             'Result: Strong correlations detected → H5 FALSIFIED',
             ha='center', va='center', transform=ax3.transAxes, fontsize=10,
             bbox=dict(boxstyle='round', facecolor='#FFF3E0', edgecolor='#FF9800', alpha=0.9))

    # === Panel D: Per-Particle Correlation Bar Chart ===
    ax4 = fig.add_subplot(gs[1, 1])

    particles = ['P1', 'P2', 'P3', 'P4', 'P5']
    correlations = [0.714, -0.061, 0.510, 0.635, 0.478]
    abs_correlations = [abs(c) for c in correlations]

    colors = ['#E74C3C' if c > 0.05 else '#2ECC71' for c in abs_correlations]
    bars = ax4.barh(particles, abs_correlations, color=colors, edgecolor='black', linewidth=1.5, height=0.6)

    ax4.axvline(x=0.05, color='red', linestyle='--', linewidth=2, label='Threshold (0.05)')
    ax4.axvline(x=np.mean(abs_correlations), color='blue', linestyle='-', linewidth=2.5,
                label=f'Mean |r| = {np.mean(abs_correlations):.3f}')

    for i, (bar, val) in enumerate(zip(bars, abs_correlations)):
        ax4.text(val + 0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', fontsize=10, fontweight='bold')

    ax4.set_xlabel('Absolute Correlation |r|', fontsize=12)
    ax4.set_ylabel('Particle ID', fontsize=12)
    ax4.set_title('(D) Per-Particle Absolute Correlations (H5)', fontsize=12, fontweight='bold')
    ax4.set_xlim(0, 0.9)
    ax4.legend(loc='lower right', fontsize=10)
    ax4.grid(True, alpha=0.3, axis='x')

    ax4.text(0.75, 0.95, '■ Exceeds threshold\n■ Below threshold',
             transform=ax4.transAxes, fontsize=9, va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    ax4.text(0.755, 0.95, '■', transform=ax4.transAxes, fontsize=9, va='top', color='#E74C3C')
    ax4.text(0.755, 0.88, '■', transform=ax4.transAxes, fontsize=9, va='top', color='#2ECC71')

    plt.tight_layout()
    plt.savefig('figure6_benchmark_results.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('figure6_benchmark_results.pdf', bbox_inches='tight', facecolor='white')
    print("Saved Figure 6: Benchmark Results with Step 4 Table")
    plt.close()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    create_figure_6_benchmark_results()
