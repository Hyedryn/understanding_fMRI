"""Simulate T2* with interactive slider plot."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import matplotlib as mpl
mpl.use('Qt5Agg')

# =============================================================================
def relaxation_T1(time, S0=100, T1=1000):
    return S0 * (1 - np.exp(-time/T1))


def update(val):
    S0 = sS0.val
    T1 = sT1.val
    l.set_ydata(relaxation_T1(time, S0=S0, T1=T1))
    fig.canvas.draw_idle()


# =============================================================================
# Prepare signal
T1 = 1000
S0 = 100
time = np.linspace(0, 4000, 4001)
signal = relaxation_T1(time, S0, T1)

# Prepare figure
fig, ax = plt.subplots()
ax.set_title(r"$S_0 * (1 - \exp(-t / T_{1}))$")
ax.set_xlabel("Time [ms]")
ax.set_ylabel("MRI signal")

plt.subplots_adjust(left=0.25, bottom=0.35)
plt.plot(time, signal, lw=3, color="red")  # initial curve
l, = plt.plot(time, signal, lw=3)
ax.margins(x=0)


# Sliders
axcolor = 'lightgoldenrodyellow'
axS0 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
axT1 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

sS0 = Slider(axS0, "$S_0$", 0, 200, valinit=100, valstep=10)
sT1 = Slider(axT1, r"$T_{1}$", 1, 2000, valinit=1000, valstep=1)

sS0.on_changed(update)
sT1.on_changed(update)

plt.show()
