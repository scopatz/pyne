from __future__ import print_function

import nose
from nose.tools import assert_equal, assert_almost_equal

from pyne.kinf import relax1g


def check_k_phi(f, kwargs, kexp, phiexp):
    kobs, phiobs = f(**kwargs)
    print("-" * 20)
    print("kexp={0}, phiexp={1}".format(kexp, phiexp))
    print("kobs={0}, phiobs={1}".format(kobs, phiobs))
    assert_almost_equal(1.0, kobs/kexp)
    assert_almost_equal(1.0, phiobs/phiexp)


def test_relax1g():
    cases = [
         # kwargs                                                  k    phi
        (dict(Sigma_f=1.0, Sigma_a=1.0, nu=1.0, k0=1.0, phi0=1.0), 1.0, 1.0),
        (dict(Sigma_f=1.0, Sigma_a=1.0, nu=1.0, k0=1.0, phi0=1e14), 1.0, 1e14),
        (dict(Sigma_f=1.0, Sigma_a=1.0, nu=2.0, k0=1.01, phi0=1e14), 
                                                                2.0, 2.0*1e14/1.01),
        (dict(Sigma_f=1.0, Sigma_a=1.0, nu=2.0, k0=2.0, phi0=2.0*1e14/1.01), 
                                                                2.0, 2.0*1e14/1.01),
        (dict(Sigma_f=0.5, Sigma_a=1.0, nu=2.0, k0=1.0, phi0=1e14), 1.0, 1e14),
        (dict(Sigma_f=0.5, Sigma_a=1.0, nu=2.0, k0=1.01, phi0=1e14), 1.0, 1e14/1.01),
        (dict(Sigma_f=0.1, Sigma_a=1.0, nu=2.0, k0=1.0395891, phi0=1e14), 1.0, 1e14/1.01),
        ]
    for kwargs, kexp, phiexp in cases:
        yield check_k_phi, relax1g, kwargs, kexp, phiexp
    


if __name__ == "__main__":
    nose.runmodule()
