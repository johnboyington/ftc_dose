import numpy as np
from pyevtk.hl import gridToVTK


def run(fname):
    print(fname)
    f = open(fname + '.imsht', 'r').readlines()

    Xs = np.array(f[9].split()[2:]).astype(float)
    Ys = np.array(f[10].split()[2:]).astype(float)
    Zs = np.array(f[11].split()[2:]).astype(float)
    Es = np.array(f[12].split()[3:]).astype(float)

    nX = len(Xs) - 1
    nY = len(Ys) - 1
    nZ = len(Zs) - 1
    nE = len(Es) - 1

    print('making mesh')
    cx = []
    cy = []
    cz = []

    for x in Xs:
        for y in Ys:
            for z in Zs:

                cx.append(x)
                cy.append(y)
                cz.append(z)

    shape = (len(Xs), len(Ys), len(Zs))

    cx = np.array(cx).reshape(shape)
    cy = np.array(cy).reshape(shape)
    cz = np.array(cz).reshape(shape)

    data = np.zeros((nE+1, nX, nY, nZ))
    error = np.zeros((nE+1, nX, nY, nZ))

    print('reading data')
    for line in f[15:]:
        E, X, Y, Z, phi, err, V, phiV = line.split()

        if E == 'Total':
            E = 0
        else:
            E = np.searchsorted(Es, float(E))

        X = np.searchsorted(Xs, float(X)) - 1
        Y = np.searchsorted(Ys, float(Y)) - 1
        Z = np.searchsorted(Zs, float(Z)) - 1
        data[E,X,Y,Z] = float(phi) * (2.13696e+26 / 2.98189e19)
        if err == 0:
            error[E,X,Y,Z] = 1.0
        else:
            error[E,X,Y,Z] = err

    print('minimum value:  {}'.format(np.min(data[data > 0])))

    print('making vtk file')
    phi = {'group{}'.format(g) if g > 0 else 'total':phi for g, phi in enumerate(data)}
    gridToVTK('./{}'.format(fname), cx, cy, cz, cellData=phi)

    print('making vtk file for error')
    phi = {'group{}'.format(g) if g > 0 else 'total':phi for g, phi in enumerate(error)}
    gridToVTK('./{}err'.format(fname), cx, cy, cz, cellData=phi)

if __name__ == '__main__':
    run('case2')
