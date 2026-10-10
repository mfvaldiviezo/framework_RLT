import traceback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

try:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    axes[0].plot([0, 1], [0, 1], label="Identidad Teórica (y = x)")
    axes[0].legend()
    axes[1].hist([0.1, 0.2, 0.5])
    bars = axes[2].bar(['A', 'B'], [1.0, 2.0])
    axes[2].set_title(r"Sensibilidad: $\mathcal{W}_1$")
    plt.tight_layout()
    plt.savefig('test_plot.png', dpi=150)
    plt.savefig('test_plot.pdf')
    print("PLOTS SAVED SUCCESSFULLY!")
except Exception:
    traceback.print_exc()
