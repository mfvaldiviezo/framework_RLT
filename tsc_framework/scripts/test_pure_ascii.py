# -*- coding: utf-8 -*-
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Testing pure ASCII plot...")
fig, ax = plt.subplots()
ax.plot([1, 2], [3, 4], label="Identity")
ax.legend()
plt.savefig("test_pure_ascii.png")
print("SUCCESS: Pure ASCII plot created!")
