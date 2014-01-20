"""This module provides capabilities to solve for the k-infinitiy multiplication 
factor.
"""

from warnings import warn

from libc.math cimport fabs

cimport numpy as np
import numpy as np



def relax1g(double Sigma_f, double Sigma_a, double nu=2.43, double k0=1.0, 
            double phi0=5e14, double tol=1e-7, int nmax=1000):
    """relax1g(double Sigma_f, double Sigma_a, double nu=2.43, double k0=1.0, 
               double phi0=5e14, double tol=1e-7, int nmax=1000)
    This is a simple one group iterative (relaxation) method for solving
    for the flux and the multiplication factor simeltaneously. This solves the 
    relative simple set of equations, where *n* is the iteration number:

    .. math::

        \phi_{n+1} = \frac{1}{k_n} \frac{\nu\Sigma_f}{\Sigma_a}\phi_n

        k_{n+1} = k_n \frac{\phi_{n+1}}{\phi_n}

    
    Parameters
    ----------
    Sigma_f : float
        Macroscopic fission cross section [1/cm].
    Sigma_a : float
        Macroscopic absorption cross section [1/cm].
    nu : float, optional
        Average number of neutrons produced per fission.
    k0 : float, optional
        Intial guess for the multiplication factor [unitless].
    phi0 : float, optional
        Initial guess for the flux [n/cm^2/s].
    tol : float, optional
        Fractional tolerance [unitless].
    nmax : int, optional
        Maximum number of iterations.

    Returns
    -------
    k : float
        The multiplication factor [unitless].
    phi : float
        The flux [n/cm^2/s].

    Notes
    -----
    This is only valid in a multiplying medium.  If k=0, then this will fail.
    Similarly, if the flux is zero then the result for k is indeterminant.

    """
    cdef int n = 0
    cdef double k_
    cdef double phi_
    cdef double k1
    cdef double phi1 
    cdef double coef = nu * Sigma_f / Sigma_a
    while ((fabs(phi1/phi0 - 1.0) > tol) or (fabs(k1/k0 - 1.0) > tol)) and (n < nmax):
        k_ = k1
        phi_ = phi1
        phi1 = coef * phi0 / k0
        k1 = k0 * phi1 / phi0 
        k0 = k_
        phi0 = phi_
        n += 1
    if n == nmax:
        warn("maximum number of iterations ({0}) reached".format(nmax), RuntimeWarning)
    return k1, phi1
