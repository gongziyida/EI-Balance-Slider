import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.colors import TwoSlopeNorm
from container import MeanInput

class SliderSpec(Slider):
    def on_changed(self, func):
        return super().on_changed(lambda v: func(self.label.get_text(), v))

def im_range(eq):
    vmin, vmax = eq.min(), eq.max()
    if vmin > 0: # +- vmax covers all
        return -vmax, vmax
    elif vmax < 0: # +- vmin covers all
        return vmin, -vmin
    else: 
        assert vmin < 0 and vmax > 0
        v = max(vmax, -vmin)
        return -v, v
    
def format_str(rEmins, rImins):
    if hasattr(rEmins, '__iter__'):
        rEstr = ', '.join(map(lambda v: '%.3f' % v, rEmins))
        rIstr = ', '.join(map(lambda v: '%.3f' % v, rImins))
    else:
        rEstr = '%.3f' % rEmins
        rIstr = '%.3f' % rImins
    return rEstr, rIstr

if __name__ == '__main__':
    p = MeanInput()

    # Create the figure and the line that we will manipulate
    fig, ax = plt.subplots(1, 3, figsize=(8, 5))
    eq, eqE, eqI, eqEmin, eqImin, rEmins, rImins = p.landscapes()
    eqE = TwoSlopeNorm(vcenter=0.)(eqE)
    eqI = TwoSlopeNorm(vcenter=0.)(eqI)
    extent = [*p.r_range, *p.r_range]
    im0 = ax[2].imshow(eq, origin='lower', extent=extent, cmap='Greys')
    imE = ax[0].imshow(eqE, origin='lower', extent=extent, cmap='Spectral')
    imI = ax[1].imshow(eqI, origin='lower', extent=extent, cmap='Spectral')
    marker0, = ax[2].plot(rEmins, rImins, marker='o', c='r', ms='8')
    markerE, = ax[0].plot(rEmins, rImins, marker='o', c='r', ms='8')
    markerI, = ax[1].plot(rEmins, rImins, marker='o', c='r', ms='8')
    for i in range(3):
        ax[i].set_xlabel('rE')
        ax[i].set_ylabel('rI')
    ax[0].set_title('Mean Input to E')
    ax[1].set_title('Mean Input to I')
    ax[2].set_title('Sum of Abs Mean Inputs')


    # adjust the main plot to make room for the sliders
    fig.subplots_adjust(bottom=0.6)

    tx1 = fig.text(0.2, 0.42, 'rE* = %s, rI* = %s\neqE* = %.3f, eqI* = %.3f' % \
                   (*format_str(rEmins, rImins), eqEmin, eqImin))
    tx2 = fig.text(0.5, 0.42, ('EE/IE = %.2f, EI/II = %.2f, EX/IX = %.2f\n'+ \
                               'IE/II = %.2f, sqrt(K_I/K_E) = %.2f') % \
                   p.ratios())
    
    # The function to be called anytime a slider's value changes
    def update(key, val):
        setattr(p, key, val)
        eq, eqE, eqI, eqEmin, eqImin, rEmins, rImins = p.landscapes()
        eqE = TwoSlopeNorm(vcenter=0.)(eqE)
        eqI = TwoSlopeNorm(vcenter=0.)(eqI)
        tx1.set_text('rE* = %s, rI* = %s\neqE* = %.3f, eqI* = %.3f' % \
                     (*format_str(rEmins, rImins), eqEmin, eqImin))
        tx2.set_text(('EE/IE = %.2f, EI/II = %.2f, EX/IX = %.2f\n'+ \
                      'IE/II = %.2f, sqrt(K_I/K_E) = %.2f') % p.ratios())
        extent = [*p.r_range, *p.r_range]
        im0.set_data(eq)
        imE.set_data(eqE)
        imI.set_data(eqI)
        marker0.set_data([rEmins, rImins])
        markerE.set_data([rEmins, rImins])
        markerI.set_data([rEmins, rImins])
        fig.canvas.draw_idle()

    # # Make horizontal sliders
    ax_sliders = {}
    for i, n in enumerate(('JEE', 'JEI', 'JEX', 'JIE', 'JII', 'JIX', 'rX')):
        ax_sl = fig.add_axes([0.2, i*0.05+0.07, 0.65, 0.03])
        sl = SliderSpec(
            ax=ax_sl,
            label=n,
            valmin=0.0,
            valmax=0.5,
            valinit=getattr(MeanInput, n),
        )
        sl.on_changed(update) # register the update function with each slider
        ax_sliders[n] = (ax_sl, sl)

    # Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
    resetax = fig.add_axes([0.8, 0.02, 0.1, 0.04])
    def reset(event):
        p.reset()
        tx1.set_text('rE* = %s, rI* = %s\neqE* = %.3f, eqI* = %.3f' % \
                     (*format_str(rEmins, rImins), eqEmin, eqImin))
        tx2.set_text(('EE/IE = %.2f, EI/II = %.2f, EX/IX = %.2f\n'+ \
                      'IE/II = %.2f, sqrt(K_I/K_E) = %.2f') % p.ratios())
        for k, (a, s) in ax_sliders.items():
            s.reset()
    button = Button(resetax, 'Reset', hovercolor='0.975')
    button.on_clicked(reset)
    
    plt.show()
