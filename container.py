import numpy as np

class MeanInput:
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
    r_range = (0, 1)
    def __init__(self, resolution=500):
        self.res = resolution
        self._r = np.linspace(*MeanInput.r_range, num=resolution)
        self._rE, self._rI = np.meshgrid(self._r, self._r)
    
    def landscapes(self):
        gamma_I = np.sqrt(self.KI) / np.sqrt(self.KE)
        gamma_X = np.sqrt(self.KX) / np.sqrt(self.KE)
        eqE = self.JEE * self._rE - \
              gamma_I * np.abs(self.JEI) * self._rI + \
              gamma_X * self.JEX * self.rX
        eqI = self.JIE * self._rE - \
              gamma_I * np.abs(self.JII) * self._rI + \
              gamma_X * self.JIX * self.rX

        eq = np.abs(eqE) + np.abs(eqI)
        rImin_idx, rEmin_idx = np.unravel_index(eq.argmin(), eqE.shape)
        rEmins, rImins = self._r[rEmin_idx], self._r[rImin_idx]
        eqEmin, eqImin = eqE[rEmin_idx, rImin_idx], eqI[rEmin_idx, rImin_idx]
        
        return eq, eqE, eqI, eqEmin, eqImin, rEmins, rImins
    
    def ratios(self):
        return self.JEE/self.JIE, self.JEI/self.JII, self.JEX/self.JIX, \
               self.JIE/self.JII, np.sqrt(self.KI/self.KE)
    
    def reset(self):
        for i in ('NE','NI','NX','KE','KI','KX',
                  'JEE','JEI','JEX','JIE','JII','JIX','rX', 'r_range'):
            setattr(self, i, getattr(MeanInput, i))
