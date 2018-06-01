import numpy as np
from senior_design_template import template


###############################################################################
#                        user defined parameters
###############################################################################

# select case
case = 1

# case 1 -> Steel Collimator Inserted, Fuel Rod in Line-of-Sight
# case 2 -> Collimator Removed, Fuel Rod Raised

###############################################################################

if case == 1:
    input_name = 'case1.i'
    plug_type = 2
    fuel_height = 0

if case == 2:
    input_name = 'case2.i'
    plug_type = 3
    fuel_height = 23

###############################################################################


def cardWriter(card, data, elements):
    '''
    Function: cardWriter

    This will write multiline cards for SI and SP distributions for mcnp inputs

    Input Data:
        card - name and number of the card
        data array - a numpy array containing the data you'd like placed in the card.
        Outputs:
            a string that can be copied and pasted into an mcnp input file
    '''
    s = '{}   '.format(card)
    empty_card = '   ' + ' ' * len(card)
    elements_per_row = elements
    row_counter = 0
    element = '{:6}  ' if data.dtype in ['int32', 'int64'] else '{:14.6e}  '
    for i, d in enumerate(data):
        s += element.format(d)
        row_counter += 1
        if row_counter == elements_per_row and i + 1 != len(data):
            row_counter = 0
            s += '\n{}'.format(empty_card)
    s += '\n'
    return s


def write_cask(inputname, plug, height):
    '''
    writes an mcnp input file for the fuel storage cask

    inputs:
    plug - type of plug
            1 - lead
            2 - steel
            3 - air
    height - the z position (cm) of the fuel rod center
             relative to the collimator hole
    '''

    # select plug
    # lead
    if plug == 1:
        s_plug = '1  -11.34'
    # steel
    elif plug == 2:
        s_plug = '2  -7.82'
    # air
    elif plug == 3:
        s_plug = '3 -0.001205'
    else:
        print('Not a valid plug option!')

    h_c = height + 5.08
    h_bot = h_c - 19.05

    # load in source spectrum
    data = np.loadtxt('source_spectra/element_3684.txt', skiprows=6)
    data = np.array(list(data[::2]) + [list(data[-1])])
    source_erg = data[:, 0]
    source_vals = data[:, 1]
    s_source = ''
    s_source += cardWriter('SI3  H ', source_erg, 4)
    s_source += cardWriter('SP3    ', source_vals, 4)

    # calculate unit conversion
    tally_multiplier = np.sum(source_vals) * 1E5 * 3600  # 1/s * mrem/Sv * s/hr

    inp = template.format(s_plug, h_bot, h_bot, s_source, tally_multiplier)

    with open(inputname, 'w+') as F:
        F.write(inp)

if __name__ == '__main__':
    write_cask(input_name, plug_type, fuel_height)
