import numpy as np
import numpy.linalg as npla


def proj(v0, v1):
    return np.dot(v0, v1) / np.dot(v1, v1) * v1


# https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process
def gram_schmidt(vs, norm=False):
    us = []
    for v in vs:
        w = v.astype(float) - sum(proj(v, u) for u in us)
        us.append(w / npla.norm(w) if norm else w)
    return us


def volume(basis):
    return abs(npla.det(basis))


# https://en.wikipedia.org/wiki/Lattice_reduction
def gaussian_lr(v0, v1):
    if np.dot(v0, v0) < np.dot(v1, v1):
        v0, v1 = v1, v0
    while np.dot(v0, v0) >= np.dot(v1, v1):
        q = round(np.dot(v0, v1 / np.dot(v1, v1)))
        v0, v1 = v1, v0 - q * v1
    return v0, v1


if __name__ == '__main__':
    _vs = (np.array([4, 1, 3, -1]), np.array([2, 1, -3, 4]), np.array([1, 0, -2, 7]), np.array([6, 2, 9, -5]))
    assert npla.norm(_vs[0]) ** 2 == _vs[0].dot(_vs[0])

    _us = gram_schmidt(_vs, True)
    assert npla.norm(_us[0]) == 1 and np.dot(_us[0], _us[1]) == 0

    assert round(volume(np.array([[6, 2, -3], [5, 1, 4], [2, 7, 1]]))) == 255

    _v0, _v1 = np.array([87502093, 123094980], dtype=object), np.array([846835985, 9834798552], dtype=object)
    _u0, _u1 = gaussian_lr(_v0, _v1)
    assert (_u0 == np.array([87502093, 123094980])).all()
    assert (_u1 == np.array([-4053281223, 2941479672])).all()
    # cannot work with object
    # assert volume(np.array([_v0, _v1])) == volume(np.array([_u0, _u1]))
    # assert max(npla.norm(_u0), npla.norm(_u1)) < max(npla.norm(_v0), npla.norm(_v1))
