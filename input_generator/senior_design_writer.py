import numpy as np
from senior_design_template import template


###############################################################################
#                        user defined parameters
###############################################################################

plug_type = 3
fuel_height = 24

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


def write_cask(plug, height):
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
    source_erg, source_probs = np.loadtxt('source.txt', skiprows=6, unpack=True)
    s_source = ''
    s_source += cardWriter('SI3  H ', source_erg[::2], 4)
    s_source += cardWriter('SP3    ', source_probs[::2], 4)

    inp = template.format(s_plug, h_bot, h_bot, s_source)

    with open('input.i', 'w+') as F:
        F.write(inp)

if __name__ == '__main__':
    write_cask(plug_type, fuel_height)
