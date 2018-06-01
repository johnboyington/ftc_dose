import numpy as np
import matplotlib.pyplot as plt
from spectrum import Spectrum

# ------------------------- grab data --------------------------------


def grab_data(filename):
    data = np.loadtxt(filename, skiprows=6)
    data = np.array(list(data[::2]) + [list(data[-1])])
    erg = data[:, 0]
    vals = data[:-1, 1]
    return Spectrum(erg, vals)


# element 3684
element_3684 = grab_data('element_3684.txt')


# ------------------------- plot --------------------------------
fig = plt.figure(0)
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-3, 10)
ax.set_ylim(1e10, 5e15)
ax.set_xlabel('Energy (MeV)')
ax.set_ylabel('Activity (Bq)')

ax.plot(element_3684.stepu_x, element_3684.stepu_y, 'b', label='Element 3684')

ax.legend()
fig.savefig('source_terms.png', dpi=300)


# --------------------- total activity ----------------------------
print('Element 3684:  {:6.4e} 1/s'.format(element_3684.total_flux))
