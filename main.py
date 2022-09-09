import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# The parametrized function to be plotted
def f(KE, KI, KX, JEE, JEI, JEX, JIE, JII, JIX, rX, r_range=(0, 1), res=500):
    _r = np.linspace(*r_range, num=res)
    rE, rI = np.meshgrid(_r, _r)
    
    gamma_I = np.sqrt(KI / KE)
    gamma_X = np.sqrt(KX / KE)
    eq1 = np.abs(JEE * rE - gamma_I * np.abs(JIE) * rI + gamma_X * JEX * rX)
    eq2 = np.abs(JIE * rE - gamma_I * np.abs(JII) * rI + gamma_X * JIX * rX)
    
    rEmin_idx, rImin_idx = np.unravel_index((np.abs(eq1) + np.abs(eq2)).argmin(), eq1.shape)
    rEmins, rImins = _r[rEmin_idx], _r[rImin_idx]
    
    return _r, eq1, eq2, rEmins, rImins

if __name__ == "__main__":
    # Define initial parameters
    NE, NI, NX = 20000, 5000, 5000
    KE = NE * 0.04
    KI = NI * 0.04
    KX = NX * 0.04
    JEE = 0.04
    JEI = 0.11
    JIE = 0.02
    JII = 0.05
    JEX = 0.06
    JIX = 0.02
    rX = 0.1

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots(1, 2, figsize=(10, 5), sharey='all', sharex='all')
    r_vals, eqE, eqI, rEmins, rImins = f(KE, KI, KX, JEE, JEI, JEX, JIE, JII, JIX, rX)
    extent = [r_vals[0], r_vals[-1], r_vals[0], r_vals[-1]]
    imE = ax[0].imshow(eqE, origin='lower', extent=extent)
    imI = ax[1].imshow(eqI, origin='lower', extent=extent)
    markerE, = ax[0].plot(rEmins, rImins, marker='o', c='r', ms='8')
    markerI, = ax[1].plot(rEmins, rImins, marker='o', c='r', ms='8')
    ax[0].set_xlabel('rE')
    ax[0].set_ylabel('rI')
    ax[0].set_title('Mean Input to E')
    ax[1].set_title('Mean Input to I')

    fig.tight_layout()

    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(left=0.25, bottom=0.25)

    # The function to be called anytime a slider's value changes
    def update(val):
        r_vals, eqE, eqI, rEmins, rImins = f(KE, KI, KX, JEE, JEI, JEX, JIE, JII, JIX, rX)
        imE.set_data(eqE)
        imI.set_data(eqI)
        markerE.set_data([rEmins, rImins])
        markerI.set_data([rEmins, rImins])
        fig.canvas.draw_idle()

    # # Make horizontal sliders
    ax_sliders = {}
    for i, (n, v) in enumerate(zip(('JEE', 'JEI', 'JEX', 'JIE', 'JII', 'JIX', 'rX'), 
                                   (JEE, JEI, JEX, JIE, JII, JIX, rX))):
        ax_sl = plt.axes([0.25, 0.1-i*0.05, 0.65, 0.03])
        sl = Slider(
            ax=ax_sl,
            label=n,
            valmin=0.0,
            valmax=1,
            valinit=v,
        )
        sl.on_changed(update) # register the update function with each slider

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = plt.axes([0.8, 0.15, 0.1, 0.04])
    def reset(event):
        freq_slider.reset()
        amp_slider.reset()
    button = Button(resetax, 'Reset', hovercolor='0.975')
    button.on_clicked(reset)
    
    plt.show()