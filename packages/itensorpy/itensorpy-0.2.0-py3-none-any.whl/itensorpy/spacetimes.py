"""
Module with pre - defined spacetime metrics commonly used in general relativity.
"""

import sympy as sp
from sympy import diag, sin, cos, exp, symbols, Symbol, Matrix
from typing import List, Optional, Tuple, Dict

from .metric import Metric


def minkowski(coordinates: Optional[List[Symbol]] = None) -> Metric:
    """
    Create a Minkowski metric for flat spacetime.

    Args:
        coordinates: Optional list of symbols [t, x, y, z]. If not provided,
                    default symbols will be created.

    Returns:
        Metric instance for Minkowski spacetime
    """
    if coordinates is None:
        t, x, y, z = symbols('t x y z')
        coordinates = [t, x, y, z]

    if len(coordinates) != 4:
        raise ValueError("Minkowski metric requires exactly 4 coordinates")

    # Metric with signature (-,+,+,+)
    g = Matrix([
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    return Metric(components=g, coordinates=coordinates)


def schwarzschild(coordinates: Optional[List[Symbol]] = None, parameters: Optional[List[Symbol]] = None) -> Metric:
    """
    Create a Schwarzschild metric for spherically symmetric spacetime.

    Args:
        coordinates: Optional list of symbols [t, r, theta, phi]. If not provided,
                    default symbols will be created.
        parameters: Optional list containing the mass parameter M. If not provided,
                   default symbol will be created.

    Returns:
        Metric instance for Schwarzschild spacetime
    """
    if coordinates is None:
        t, r, theta, phi = symbols('t r theta phi')
        coordinates = [t, r, theta, phi]

    if len(coordinates) != 4:
        raise ValueError("Schwarzschild metric requires exactly 4 coordinates")

    t, r, theta, phi = coordinates

    if parameters is None:
        M = Symbol('M', positive=True)
        parameters = [M]
    else:
        M = parameters[0]

    # Schwarzschild metric components
    g_tt = -(1 - 2 * M/r)
    g_rr = 1/(1 - 2 * M/r)
    g_theta_theta = r**2
    g_phi_phi = r**2 * sin(theta)**2

    # Create the metric matrix directly
    g = Matrix([
        [g_tt, 0, 0, 0],
        [0, g_rr, 0, 0],
        [0, 0, g_theta_theta, 0],
        [0, 0, 0, g_phi_phi]
    ])

    return Metric(components=g, coordinates=coordinates, params=parameters)


def reissner_nordstrom(coordinates: Optional[List[Symbol]] = None, parameters: Optional[List[Symbol]] = None) -> Metric:
    """
    Create a Reissner - Nordström metric for charged black holes.

    Args:
        coordinates: Optional list of symbols [t, r, theta, phi]. If not provided,
                    default symbols will be created.
        parameters: Optional list containing [M, Q] for mass and charge.
                   If not provided, default symbols will be created.

    Returns:
        Metric instance for Reissner - Nordström spacetime
    """
    if coordinates is None:
        t, r, theta, phi = symbols('t r theta phi')
        coordinates = [t, r, theta, phi]

    if len(coordinates) != 4:
        raise ValueError("Reissner - Nordström metric requires exactly 4 coordinates")

    t, r, theta, phi = coordinates

    if parameters is None:
        M = Symbol('M', positive=True)
        Q = Symbol('Q', real=True)
        parameters = [M, Q]
    else:
        M, Q = parameters[:2]

    # Reissner - Nordström metric components
    g_tt = -(1 - 2 * M/r + Q**2 / r**2)
    g_rr = 1/(1 - 2 * M/r + Q**2 / r**2)
    g_theta_theta = r**2
    g_phi_phi = r**2 * sin(theta)**2

    # Create the metric matrix directly
    g = Matrix([
        [g_tt, 0, 0, 0],
        [0, g_rr, 0, 0],
        [0, 0, g_theta_theta, 0],
        [0, 0, 0, g_phi_phi]
    ])

    return Metric(components=g, coordinates=coordinates, params=parameters)


def kerr(coordinates: Optional[List[Symbol]] = None, parameters: Optional[List[Symbol]] = None) -> Metric:
    """
    Create a Kerr metric for rotating black holes.

    Args:
        coordinates: Optional list of symbols [t, r, theta, phi]. If not provided,
                    default symbols will be created.
        parameters: Optional list containing [M, a] for mass and angular momentum.
                   If not provided, default symbols will be created.

    Returns:
        Metric instance for Kerr spacetime
    """
    if coordinates is None:
        t, r, theta, phi = symbols('t r theta phi')
        coordinates = [t, r, theta, phi]

    if len(coordinates) != 4:
        raise ValueError("Kerr metric requires exactly 4 coordinates")

    t, r, theta, phi = coordinates

    if parameters is None:
        M = Symbol('M', positive=True)
        a = Symbol('a', real=True)
        parameters = [M, a]
    else:
        M, a = parameters[:2]

    # Auxiliary functions for Kerr metric
    rho_squared = r**2 + (a * cos(theta))**2
    delta = r**2 - 2 * M*r + a**2
    sigma = (r**2 + a**2)**2 - a**2 * delta * sin(theta)**2

    # Create metric components dictionary
    components = {}

    # Diagonal components
    components[(0, 0)] = -1 + 2 * M*r / rho_squared  # g_tt
    components[(1, 1)] = rho_squared / delta  # g_rr
    components[(2, 2)] = rho_squared  # g_theta_theta
    components[(3, 3)] = (r**2 + a**2 + 2 * M*r * a**2 * sin(theta)**2 / rho_squared) * sin(theta)**2  # g_phi_phi

    # Off - diagonal components
    components[(0, 3)] = -2 * M*r * a*sin(theta)**2 / rho_squared  # g_t_phi = g_phi_t

    # Create the metric tensor
    return Metric(components=components, coordinates=coordinates, params=parameters)


def friedmann_lemaitre_robertson_walker(coordinates: Optional[List[Symbol]] = None,
                                         parameters: Optional[List[Symbol]] = None,
                                         k: int = 0) -> Metric:
    """
    Create a Friedmann - Lemaître - Robertson - Walker (FLRW) metric for cosmology.

    Args:
        coordinates: Optional list of symbols [t, r, theta, phi]. If not provided,
                    default symbols will be created.
        parameters: Optional list containing the scale factor a(t). If not provided,
                   default symbol will be created.
        k: Curvature parameter: 0 (flat), 1 (closed), -1 (open). Default is 0.

    Returns:
        Metric instance for FLRW spacetime
    """
    if coordinates is None:
        t, r, theta, phi = symbols('t r theta phi')
        coordinates = [t, r, theta, phi]

    if len(coordinates) != 4:
        raise ValueError("FLRW metric requires exactly 4 coordinates")

    t, r, theta, phi = coordinates

    if parameters is None:
        a = sp.Function('a')(t)
        parameters = [a]
    else:
        a = parameters[0]

    # Compute the radial component of the spatial metric
    if k == 0:
        # Flat space
        radial_factor = 1
    elif k == 1:
        # Closed space (positive curvature)
        radial_factor = 1/(1 - k * r**2)
    elif k == -1:
        # Open space (negative curvature)
        radial_factor = 1/(1 - k * r**2)
    else:
        raise ValueError("k must be one of {-1, 0, 1}")

    # FLRW metric components
    g_tt = -1
    g_rr = a**2 * radial_factor
    g_theta_theta = a**2 * r**2
    g_phi_phi = a**2 * r**2 * sin(theta)**2

    # Create the metric matrix directly
    g = Matrix([
        [g_tt, 0, 0, 0],
        [0, g_rr, 0, 0],
        [0, 0, g_theta_theta, 0],
        [0, 0, 0, g_phi_phi]
    ])

    return Metric(components=g, coordinates=coordinates, params=parameters)


def de_sitter(coordinates: Optional[List[Symbol]] = None, parameters: Optional[List[Symbol]] = None) -> Metric:
    """
    Create a de Sitter metric for spacetime with positive cosmological constant.

    Args:
        coordinates: Optional list of symbols [t, r, theta, phi]. If not provided,
                    default symbols will be created.
        parameters: Optional parameter for cosmological constant H. If not provided,
                   default symbol will be created.

    Returns:
        Metric instance for de Sitter spacetime
    """
    if coordinates is None:
        t, r, theta, phi = symbols('t r theta phi')
        coordinates = [t, r, theta, phi]

    if len(coordinates) != 4:
        raise ValueError("de Sitter metric requires exactly 4 coordinates")

    t, r, theta, phi = coordinates

    if parameters is None:
        H = Symbol('H', positive=True)
        parameters = [H]
    else:
        H = parameters[0]

    # de Sitter metric in static coordinates
    g_tt = -(1 - H**2 * r**2)
    g_rr = 1/(1 - H**2 * r**2)
    g_theta_theta = r**2
    g_phi_phi = r**2 * sin(theta)**2

    # Create the metric matrix directly
    g = Matrix([
        [g_tt, 0, 0, 0],
        [0, g_rr, 0, 0],
        [0, 0, g_theta_theta, 0],
        [0, 0, 0, g_phi_phi]
    ])

    return Metric(components=g, coordinates=coordinates, params=parameters)


def anti_de_sitter(coordinates: Optional[List[Symbol]] = None, parameters: Optional[List[Symbol]] = None) -> Metric:
    """
    Create an Anti - de Sitter metric for spacetime with negative cosmological constant.

    Args:
        coordinates: Optional list of symbols [t, r, theta, phi]. If not provided,
                    default symbols will be created.
        parameters: Optional parameter for AdS radius L. If not provided,
                   default symbol will be created.

    Returns:
        Metric instance for Anti - de Sitter spacetime
    """
    if coordinates is None:
        t, r, theta, phi = symbols('t r theta phi')
        coordinates = [t, r, theta, phi]

    if len(coordinates) != 4:
        raise ValueError("Anti - de Sitter metric requires exactly 4 coordinates")

    t, r, theta, phi = coordinates

    if parameters is None:
        L = Symbol('L', positive=True)
        parameters = [L]
    else:
        L = parameters[0]

    # Anti - de Sitter metric
    g_tt = -(1 + r**2 / L**2)
    g_rr = 1/(1 + r**2 / L**2)
    g_theta_theta = r**2
    g_phi_phi = r**2 * sin(theta)**2

    # Create the metric matrix directly
    g = Matrix([
        [g_tt, 0, 0, 0],
        [0, g_rr, 0, 0],
        [0, 0, g_theta_theta, 0],
        [0, 0, 0, g_phi_phi]
    ])

    return Metric(components=g, coordinates=coordinates, params=parameters)
