import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator

def create_visualization(results_df, project_root):
    """Generate high-quality comparison chart optimized for reporting"""
    # Prepare data
    pivot_df = results_df.pivot(index='Indicator', columns='Status', values='Coverage (%)')
    
    # Set up figure with optimal dimensions
    plt.figure(figsize=(12, 8))  # Increased base size
    
    # Create horizontal bar plot
    ax = pivot_df.plot(
        kind='barh',
        color=['#2ecc71', '#e74c3c'],  # Green for on-track, red for off-track
        width=0.7,
        edgecolor='white',
        linewidth=0.7
    )
    
    # Customize appearance
    plt.title('Maternal Health Coverage by U5MR Status', 
              pad=20, fontsize=14, fontweight='bold')
    plt.xlabel('Coverage (%)', labelpad=10, fontsize=12)
    plt.ylabel('', labelpad=10)  # Remove y-label as indicators are self-explanatory
    plt.xlim(0, 100)
    
    # Improve tick marks
    ax.xaxis.set_major_locator(MaxNLocator(10))
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10, rotation=0)
    
    # Add value labels inside bars
    for p in ax.patches:
        width = p.get_width()
        if width > 5:  # Only label bars wide enough to accommodate text
            ax.text(width - 5 if width > 20 else width + 2,
                    p.get_y() + p.get_height()/2,
                    f'{width:.1f}%',
                    ha='left' if width <= 20 else 'right',
                    va='center',
                    color='white' if width > 50 else 'black',
                    fontsize=10,
                    fontweight='bold')
    
    # Customize legend
    plt.legend(
        title='U5MR Status',
        bbox_to_anchor=(1, 1),
        loc='upper left',
        frameon=True,
        framealpha=1
    )
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Leave space for legend
    
    # Save high-quality image
    output_path = project_root/"results"/"coverage_comparison.png"
    plt.savefig(
        output_path,
        dpi=150,  # Increased DPI for better quality
        bbox_inches='tight',
        facecolor='white',
        quality=95
    )
    plt.close()
    print(f"Visualization saved to: {output_path}")