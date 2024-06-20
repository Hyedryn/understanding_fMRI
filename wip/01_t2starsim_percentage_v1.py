"""Simulate T2* with interactive slider plot."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import matplotlib as mpl
mpl.use('Qt5Agg')

# =============================================================================
def relaxation_T2star(time, S0=100, T2star=28):
    return S0 * np.exp(-time/T2star)

def computeT2star(T2starInital, percentage, echoTime):
    #percentage =  np.exp(-echoTime / T2starTarget   + echoTime / T2starInital)
    #np.log(percentage) = -echoTime / T2starTarget   + echoTime / T2starInital
    # T2starTarget = -echoTime / (np.log(percentage)  - echoTime / T2starInital)

    T2starTargetv1 = - np.log((1+percentage) * np.exp(-echoTime / T2starInital))/ echoTime
    T2starTarget = - echoTime / (np.log(1+percentage) - echoTime / T2starInital)
    print(T2starTarget, T2starTargetv1)
    return T2starTarget

def update(val):
    S0 = sS0.val
    T2star = sT2star.val
    l.set_ydata(relaxation_T2star(time, S0=S0, T2star=T2star))
    signal.set_text(f"MRI signal at TE {sEchoTime.val} ms : {relaxation_T2star(sEchoTime.val, S0=S0, T2star=T2star):.{3}f}")
    sPercentage.set_val(0)

def updateT2Estimate(val):
    S0 = sS0.val
    T2star = sT2star.val
    T2starTarget = computeT2star(T2star, sPercentage.val/100, sEchoTime.val)
    vline.set_xdata([sEchoTime.val, sEchoTime.val])
    text.set_text(f"T2* to have {sPercentage.val}% signal change at TE {sEchoTime.val} ms : {T2starTarget:.{3}f} ms")
    signal.set_text(
        f"MRI signal at TE {sEchoTime.val} ms : {relaxation_T2star(sEchoTime.val, S0=S0, T2star=T2star):.{3}f}")

    fig.canvas.draw_idle()

# =============================================================================
# Prepare signal
T2star = 28
S0 = 100
time = np.linspace(0, 100, 101)
signal = relaxation_T2star(time, S0, T2star)

# Prepare figure
fig, ax = plt.subplots()
ax.set_title(r"$S_0 * \exp(-t / T_{2}^*)$")
ax.set_xlabel("Time [ms]")
ax.set_ylabel("MRI signal")

plt.subplots_adjust(left=0.25, bottom=0.35)
plt.plot(time, signal, lw=3, color="red")  # initial curve
l, = plt.plot(time, signal, lw=3)

ax.margins(x=0)

# Sliders
axcolor = 'lightgoldenrodyellow'
axS0 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
axT2star = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

sS0 = Slider(axS0, "$S_0$", 0, 200, valinit=100, valstep=10)
sT2star = Slider(axT2star, r"$T_{2}^*$", 1, 100, valinit=28, valstep=1)

axPercentage = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
axEchoTime = plt.axes([0.25, 0, 0.65, 0.03], facecolor=axcolor)
sPercentage = Slider(axPercentage, "Signal change [%]", -100, 100, valinit=0, valstep=1)
sEchoTime = Slider(axEchoTime, r"Echo Time [ms]", 1, 100, valinit=40, valstep=1)
text = plt.text(0, 0.65, f"T2* to have {sPercentage.val}% signal change at TE {sEchoTime.val} ms : {T2star:.{3}f} ms")
signal = plt.text(10, 2, f"MRI signal at TE {sEchoTime.val} ms : {relaxation_T2star(sEchoTime.val, S0=S0, T2star=T2star):.{3}f}")

# Vertical Line at defined echo time
vline = ax.axvline(x=sEchoTime.val, color='k', linestyle='--')

sS0.on_changed(update)
sT2star.on_changed(update)
sEchoTime.on_changed(updateT2Estimate)
sPercentage.on_changed(updateT2Estimate)

plt.show()
