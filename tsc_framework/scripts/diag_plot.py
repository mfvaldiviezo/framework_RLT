import os, sys, traceback
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("STEP 1: Matplotlib imported")
try:
    fig, ax = plt.subplots(1, 1)
    ax.plot([1, 2], [3, 4])
    print("STEP 2: Figure created")
    plt.savefig("test_fig.png")
    print("STEP 3: Saved test_fig.png")
    plt.savefig("test_fig.pdf")
    print("STEP 4: Saved test_fig.pdf")
    plt.close()
    print("ALL STEPS COMPLETED!")
except Exception as e:
    traceback.print_exc()
