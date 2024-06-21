"""Simulate T2* with interactive slider plot."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import matplotlib as mpl
mpl.use('Qt5Agg')

def relaxation_T2star(time, S0=100, T2star=28):
    """Calculate MRI signal decay over time."""
    return S0 * np.exp(-time / T2star)

def computeT2star(T2starInitial, percentage, echoTime):
    """Compute the target T2* based on percentage signal change and echo time."""
    T2starTarget = -echoTime / (np.log(1 + percentage) - echoTime / T2starInitial)
    print(T2starTarget)
    return T2starTarget

def update(val):
    """Update the plot based on slider values."""
    S0 = sS0.val
    T2star = sT2star.val
    l.set_ydata(relaxation_T2star(time, S0=S0, T2star=T2star))
    signal.set_text(f"MRI signal at TE {sEchoTime.val} ms: {relaxation_T2star(sEchoTime.val, S0=S0, T2star=T2star):.3f}")
    sPercentage.set_val(0)

def updateT2Estimate(val):
    """Update T2* estimate and vertical line based on sliders."""
    S0 = sS0.val
    T2star = sT2star.val
    T2starTarget = computeT2star(T2star, sPercentage.val / 100, sEchoTime.val)
    vline.set_xdata([sEchoTime.val, sEchoTime.val])
    text.set_text(f"T2* for {sPercentage.val}% signal change at TE {sEchoTime.val} ms: {T2starTarget:.3f} ms")
    signal.set_text(f"MRI signal at TE {sEchoTime.val} ms: {relaxation_T2star(sEchoTime.val, S0=S0, T2star=T2star):.3f}")
    fig.canvas.draw_idle()

# Initial parameters
T2star_initial = 28
S0_initial = 100
time = np.linspace(0, 100, 101)
signal_data = relaxation_T2star(time, S0_initial, T2star_initial)

# Create figure and plot
fig, ax = plt.subplots()
ax.set_title(r"$S_0 \cdot \exp(-t / T_{2}^*)$")
ax.set_xlabel("Time [ms]")
ax.set_ylabel("MRI signal")
plt.subplots_adjust(left=0.25, bottom=0.35)

l, = ax.plot(time, signal_data, lw=3, color="red")
ax.margins(x=0)

# Slider colors and positions
axcolor = 'lightgoldenrodyellow'
axS0 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
axT2star = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axPercentage = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
axEchoTime = plt.axes([0.25, 0, 0.65, 0.03], facecolor=axcolor)

# Slider creation
sS0 = Slider(axS0, "$S_0$", 0, 200, valinit=S0_initial, valstep=10)
sT2star = Slider(axT2star, r"$T_{2}^*$", 1, 100, valinit=T2star_initial, valstep=1)
sPercentage = Slider(axPercentage, "Signal change [%]", -100, 100, valinit=0, valstep=1)
sEchoTime = Slider(axEchoTime, "Echo Time [ms]", 1, 100, valinit=40, valstep=1)

# Text annotations
text = plt.text(0, 0.65, f"T2* for {sPercentage.val}% signal change at TE {sEchoTime.val} ms: {T2star_initial:.3f} ms")
signal = plt.text(10, 2, f"MRI signal at TE {sEchoTime.val} ms: {relaxation_T2star(sEchoTime.val, S0=S0_initial, T2star=T2star_initial):.3f}")

# Vertical line for echo time
vline = ax.axvline(x=sEchoTime.val, color='k', linestyle='--')

# Connect sliders to update functions
sS0.on_changed(update)
sT2star.on_changed(update)
sEchoTime.on_changed(updateT2Estimate)
sPercentage.on_changed(updateT2Estimate)

plt.show()
