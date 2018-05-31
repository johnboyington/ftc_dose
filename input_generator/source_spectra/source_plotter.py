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

# element 3684
element_2989 = grab_data('element_2989_measured.txt')

# senior design source
data = np.loadtxt('senior_design_source.txt')
erg = data[0]
vals = data[1][1:] * 1e17  # arbitrary scaling coefficient
sr_design = Spectrum(erg, vals)


# ------------------------- plot --------------------------------
fig = plt.figure(0)
ax = fig.add_subplot(111)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-3, 10)
ax.set_ylim(1e13, 1e18)

ax.plot(element_3684.stepu_x, element_3684.stepu_y, 'b', label='Element 3684')
# ax.plot(element_2989.stepu_x, element_2989.stepu_y, 'g', label='Element 2989')
# ax.plot(sr_design.stepu_x, sr_design.stepu_y, 'r', label='Senior Design')

ax.legend()
fig.savefig('source_terms.png', dpi=300)


# --------------------- total activity ----------------------------
print('Element 3684:  {} 1/s'.format(element_3684.total_flux))
print('Element 2989:  {} 1/s'.format(element_2989.total_flux))
