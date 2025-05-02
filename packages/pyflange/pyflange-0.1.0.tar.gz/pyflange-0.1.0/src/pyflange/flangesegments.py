# pyFlange - python library for large flanges design
# Copyright (C) 2024  KCI The Engineers B.V.,
#                     Siemens Gamesa Renewable Energy B.V.,
#                     Nederlandse Organisatie voor toegepast-natuurwetenschappelijk onderzoek TNO.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, as published by
# the Free Software Foundation, either version 3 of the License, or any
# later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License version 3 for more details.
#
# You should have received a copy of the GNU General Public License
# version 3 along with this program.  If not, see <https://www.gnu.org/licenses/>.

''' This module contains ``FlangeSegment`` classes, which model the mechanical
behavior of a flange sector containig one bolt only.

Currently, the only type of FlangeSegment available is a L-Flange segmen, implementing
a polinomial relation between shell pull force and bolt force / bolt moment. Nonetheless,
this module has been structured to be easily extensible with other types of FlangeSegment
model, such as Polynomial T-Flanges, Multilinear (Petersen) L-Flanges, Multilinear T-Flanges.

The models implemented in this module are based on the following references:

[1]:  Marc Seidel, SGRE TE TF PST: Fatigue design guide for ring flange connections in wind turbine support structures.
      Background to proposed changes to IEC 61400-6
      Draft version V06

[3]:  Petersen, C.: Nachweis der Betriebsfestigkeit exzentrisch beanspruchter Ringflansch-verbindungen
      (Fatigue assessment of eccentrically loaded ring flange connections).
      Stahlbau 67 (1998), S. 191-203. https://onlinelibrary.wiley.com/doi/abs/10.1002/stab.199800690

[4]:  Petersen, C.: Stahlbau (Steel construction), 4. Auflage Braunschweig: Wiesbaden: Springer Vieweg 2012.
      https://link.springer.com/book/10.1007%2F978-3-8348-8610-1

[9]:  Tobinaga, I.; Ishihara, T.: A study of action point correction factor for L‐type flanges of wind turbine towers.
      Wind Energy 21 (2018), p. 801-806. https://doi.org/10.1002/we.2193


'''




from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import numpy as np

from .bolts import Bolt



class FlangeSegment (ABC):
    ''' Abstract FlangeSegment class, meant to be extended and
    not to be instatiated directly.

    Each FlangeSegment child class must implement the two methods
    ``.bolt_axial_force(Z)`` and ``.bolt_bending_moment(Z)``.
    '''

    @abstractmethod
    def bolt_axial_force (self, shell_pull):
        pass


    @abstractmethod
    def bolt_bending_moment (self, shell_pull):
        pass



class PolynomialFlangeSegment (FlangeSegment):
    ''' This is a generic FlangeSegment that implements a polynomial
    relation between shell pull Z and bolt axial force Fs or bolt
    bending moment Ms.

    It is not meant to be instantiated directly, but to be subclassed
    instead.

    The polynomial functions ``.bolt_axial_force(Z)`` and
    ``.bolt_bending_moment(Z)`` are defined based on 4 points, through
    which the polynomials pass. Those points are implementation specific.

    The 4 reference points for the Fs(Z) polynomial are:

    - ``P1 = (Z1, Fs1)`` representing the flange segment state at rest (no
      loads applied, other than the self-weight). Each implementatio of
      this class should define Z1 as ``shell_force_at_rest`` property and
      Fs1 as ``bolt_force_at_rest`` property.

    - ``P2 = (Z2, Fs2)`` representing the flange segment ultimate tensile
      limit state (failure state B). Each implementatio of this class should
      define Z2 as ``shell_force_at_tensile_ULS`` property and Fs2 as
      ``bolt_force_at_ultimate_ULS`` property.

    - ``P3 = (Z3, Fs3)`` representing the flange segment in small tensile
      deformation condition. This point is meant to define the initial slope
      of the polynomial. Each implementatio of this class should
      define Z3 as ``shell_force_at_small_displacement`` property and Fs3 as
      ``bolt_force_at_small_displacement`` property.

    - ``P4 = (Z4, Fs4)`` representing the gap closure state. Each implementatio
      of this class should define Z4 as ``shell_force_at_closed_gap`` property,
      while Fs4 is automatically defined.

    The 4 reference points for the Ms(Z) polynomial are:

    - ``Q1 = (Z1, Ms1)`` corresponding to P1 as defined above. Each implementation
      of this class should define Ms1 as ``bolt_moment_at_rest`` property.

    - ``Q2 = (Z2, Ms2)`` corresponding to P2 as defined above. Each implementation
      of this class should define Ms2 as ``bolt_moment_at_tensile_ULS`` property.

    - ``Q3 = (Z3, Ms3)`` corresponding to P3 as defined above. Each implementation
      of this class should define Ms3 as ``bolt_moment_at_small_displacement`` property.

    - ``Q4 = (Z4, Ms4)`` corresponding to P4 as defined above. Each implementatio
      of this class should define Z4 as ``shell_force_at_closed_gap`` property,
      while Ms4 is automatically defined.
    '''

    def bolt_axial_force (self, shell_pull):
        ''' Bolt axial force due to a given shell pull force Z.

        The relation between shell pull force Z and bolt axial force Fs,
        is a polynomial function, as defined in ref.[1], section 9.

        The passed shell_pull parameter must be either a real number or
        a numpy.array. If a numpy.array is passed, then the corresponding
        array of Fs values will be returned.
        '''

        # Retrueve the polynomial branch in the tensile domain and the
        # polynomial branch in the compressive domain. The evaluation
        # of both polynomials is delegated to a separate getter for
        # the sake of separation of concerns and code readability.
        tens_poli = self._tensile_force_polynomial
        comp_poli = self._compressive_force_polynomial

        # The tensile polynomial is defined between Z1 and Z2, while
        # the compressive prolynomila between Zmin and Z1
        Z1, Z2 = tens_poli.domain
        Zmin = comp_poli.domain[0]

        # Calculate a vector with the same size as shell_pull, having the Fs value
        # in tensile domain where shell_value is greater than Z1 and 0 in all
        # the other cases.
        Fs_tens = tens_poli(shell_pull) * (shell_pull > Z1)

        # Calculate a vector with the same size as shell_pull, having the Fs value
        # in compressive domain where shell_value is between Zmin and Z1 and 0 in all
        # the other cases.
        Fs_comp = comp_poli(shell_pull) * (shell_pull > Zmin) * (shell_pull <= Z1)

        # Calculate a vector with the same size as shell_pull, having the Fs(Zmin)
        # value where shell_value is lower than or equal to zmin and 0 in all
        # the other cases.
        Fs_min  = comp_poli(Zmin) * (shell_pull <= Zmin)

        # Compose the three branches together and return them.
        return Fs_tens + Fs_comp + Fs_min


    def bolt_bending_moment (self, shell_pull):
        ''' Bolt bending moment due to a given shell pull force Z.

        The relation between shell pull force Z and bolt bending moment Ms,
        is a polynomial function, as defined in ref.[1], section 9.

        The passed shell_pull parameter must be either a real number or
        a numpy.array. If a numpy.array is passed, then the corresponding
        array of Ms values will be returned.
        '''

        # Retrueve the polynomial branch in the tensile domain and the
        # polynomial branch in the compressive domain. The evaluation
        # of both polynomials is delegated to a separate getter for
        # the sake of separation of concerns and code readability.
        tens_poli = self._tensile_moment_polynomial
        comp_poli = self._compressive_moment_polynomial

        # The tensile polynomial is defined between Z1 and Z2, while
        # the compressive prolynomila between Zmin and Z1
        Z1, Z2 = tens_poli.domain
        Zmin = comp_poli.domain[0]

        # Calculate a vector with the same size as shell_pull, having the Ms values
        # in tensile domain where shell_value is greater than Z1 and 0 in all
        # the other cases.
        Ms_tens = tens_poli(shell_pull) * (shell_pull > Z1)

        # Calculate a vector with the same size as shell_pull, having the Ms values
        # in compressive domain where shell_value is between Zmin and Z1 and 0 in all
        # the other cases.
        Ms_comp = comp_poli(shell_pull) * (shell_pull > Zmin) * (shell_pull <= Z1)

        # Calculate a vector with the same size as shell_pull, having the Ms(Zmin)
        # value where shell_value is lower than or equal to zmin and 0 in all
        # the other cases.
        Ms_min  = comp_poli(Zmin) * (shell_pull <= Zmin)

        # Compose the three branches together and return them.
        return Ms_tens + Ms_comp + Ms_min


    @cached_property
    def _tensile_force_polynomial (self):
        ''' Polynomia Fs(Z) in the tensile domain

        This getter returns the polynomial Fs(Z) defined by ref. [1]
        between point 1 (flange semgment at rest) and point 2 (ultimate
        tensile limit state of the bolt).
        '''
        from numpy.polynomial.polynomial import Polynomial
        from numpy.linalg import inv

        # The polynomial function Fs(Z) passes through the following points
        # The point getters are implementation-specific and they should be
        # defined by the child class (L-Flange class or T-Flange class).
        Z1 = self.shell_force_at_rest
        Fs1 = self.bolt_force_at_rest

        Z2 = self.shell_force_at_tensile_ULS
        Fs2 = self.bolt_force_at_tensile_ULS

        Z3 = self.shell_force_at_small_displacement
        Fs3 = self.bolt_force_at_small_displacement

        # The three fitting conditions Fs(Z1)=Fs1, Fs(Z2)=Fs2 and Fs(Z3)=Fs3
        # are written in matrix form as: Z*A=F whenre A is the coefficients
        # vector and F and Z are defined below:
        F = np.array([Fs1, Fs2, Fs3])
        Z = np.array([
            [1, Z1, Z1**2],
            [1, Z2, Z2**2],
            [1, Z3, Z3**2]])

        # The coefficients are therefore:
        a0, a1, a2 = inv(Z) @ F

        # Create and return the polynomial for the tensile domain [Z1, Z2]
        return Polynomial(
            (a0, a1, a2),       # coefficients
            domain=(Z1, Z2),    # the polynomial is defined between Z1 and Z2
            window=(Z1, Z2),
            symbol="Z")         # used to render the independent variable in serializations


    @cached_property
    def _compressive_force_polynomial (self):
        from numpy.polynomial.polynomial import Polynomial

        # Retrieve origin of the compressive polynomial
        Z1 = self.shell_force_at_rest
        Fs1 = self.bolt_force_at_rest

        # Retrieve slope of the compressive polynomial at point (Z1, Fs1)
        dtp = self._tensile_force_polynomial.deriv()    # first derivative of the tensile polynomial
        X1 = dtp(Z1)                                    # slope of the tensile polinomial at Z=Z1

        # Value of Z below which the compressive polynomial
        # becomes practically constant
        Zmin = -self.shell_force_at_closed_gap + Z1

        # Compressive polynomial coefficients
        c2 = -0.5 * X1 / (Zmin - Z1)
        c1 = X1 - 2*c2*Z1
        c0 = Fs1 - c1*Z1 + c2*Z1**2

        # Create and return the polynomial for the tensile domain [Zmin, Z1]
        return Polynomial(
            (c0, c1, c2),       # coefficients
            domain=(Zmin, Z1),  # the polynomial is defined between Zmin and Z1
            window=(Zmin, Z1),
            symbol="Z")         # used to render the independent variable in serializations


    @cached_property
    def _tensile_moment_polynomial (self):
        from numpy.polynomial.polynomial import Polynomial
        from numpy.linalg import inv

        # The polynomial function Fs(Z) passes through the following points
        # The point getters are implementation-specific and they should be
        # defined by the child class (L-Flange class or T-Flange class).
        Z1 = self.shell_force_at_rest
        Ms1 = self.bolt_moment_at_rest

        Z2 = self.shell_force_at_tensile_ULS
        Ms2 = self.bolt_moment_at_tensile_ULS

        Z3 = self.shell_force_at_small_displacement
        Ms3 = self.bolt_moment_at_small_displacement

        # The three fitting conditions Fs(Z1)=Fs1, Fs(Z2)=Fs2 and Fs(Z3)=Fs3
        # are written in matrix form as: Z*A=F whenre A is the coefficients
        # vector and F and Z are defined below:
        M = np.array([Ms1, Ms2, Ms3])
        Z = np.array([
            [1, Z1, Z1**2],
            [1, Z2, Z2**2],
            [1, Z3, Z3**2]])

        # The coefficients are therefore:
        a0, a1, a2 = inv(Z) @ M

        # Create and return the polynomial for the tensile domain [Z1, Z2]
        return Polynomial(
            (a0, a1, a2),       # coefficients
            domain=(Z1, Z2),    # the polynomial is defined between Z1 and Z2
            window=(Z1, Z2),
            symbol="Z")         # used to render the independent variable in serializations


    @cached_property
    def _compressive_moment_polynomial (self):
        from numpy.polynomial.polynomial import Polynomial

        # Retrieve origin of the compressive polynomial
        Z1 = self.shell_force_at_rest
        Ms1 = self.bolt_moment_at_rest

        # Retrieve slope of the compressive polynomial at point (Z1, Fs1)
        dtp = self._tensile_moment_polynomial.deriv()    # first derivative of the tensile polynomial
        X1 = dtp(Z1)                                    # slope of the tensile polinomial at Z=Z1

        # Value of Z below which the compressive polynomial
        # becomes practically constant
        Zmin = -self.shell_force_at_closed_gap + Z1

        # Compressive polynomial coefficients
        c2 = -0.5 * X1 / (Zmin - Z1)
        c1 = X1 - 2*c2*Z1
        c0 = Ms1 - c1*Z1 + c2*Z1**2

        # Create and return the polynomial for the tensile domain [Zmin, Z1]
        return Polynomial(
            (c0, c1, c2),       # coefficients
            domain=(Zmin, Z1),  # the polynomial is defined between Zmin and Z1
            window=(Zmin, Z1),
            symbol="Z")         # used to render the independent variable in serializations


    @property
    @abstractmethod
    def shell_force_at_rest (self):
        pass


    @property
    @abstractmethod
    def bolt_force_at_rest (self):
        pass


    @property
    @abstractmethod
    def bolt_moment_at_rest (self):
        pass


    @property
    @abstractmethod
    def shell_force_at_small_displacement (self):
        pass


    @property
    @abstractmethod
    def bolt_force_at_small_displacement (self):
        pass


    @property
    @abstractmethod
    def bolt_moment_at_small_displacement (self):
        pass


    @property
    @abstractmethod
    def shell_force_at_tensile_ULS (self):
        pass


    @property
    @abstractmethod
    def bolt_force_at_tensile_ULS (self):
        pass


    @property
    @abstractmethod
    def bolt_moment_at_tensile_ULS (self):
        pass


    @property
    @abstractmethod
    def shell_force_at_closed_gap (self):
        pass



@dataclass
class PolynomialLFlangeSegment (PolynomialFlangeSegment):
    ''' This class provide a ``PolynomialFlangeSegment`` implementation for L-Flanges,
    based on ref. [1].

    For this particular case of flange, this class defines the polynomial reference
    points ``P1``, ``P2``, ``P3``, ``P4``, ``Q1``, ``Q2``, ``Q3``, ``Q4`` and inherits
    the polynomial functions ``.bolt_axial_force(Z)`` and ``.bolt_bending_moment(Z)``
    from the parent class.

    The parameters required by this class are:

    - ``a`` : ``float``
        Distance between inner face of the flange and center of the bolt hole.

    - ``b`` : ``float``
        Distance between center of the bolt hole and center-line of the shell.

    - ``s`` : ``float``
        Shell thickness.

    - ``t`` : ``float``
        Flange thickness.

    - ``c`` : ``float``
        Shell arc length.

    - ``R`` : ``float``
        Shell outer curvature radius.

    - ``Zg`` : ``float``
        Load applied to the flange segment shell at rest (normally dead weight
        of tower + RNA, divided by the number of bolts). Negative if compression.

    - ``bolt`` : ``Bolt``
        Bolt object representing the flange segment bolt.

    - ``Fv`` : ``float``
        Applied bolt preload, after preload losses.

    - ``Do`` : ``float``
        Bolt hole diameter.

    - ``Dw`` : ``float``
        Washer diameter.

    - ``gap_height`` : ``float``
        Maximum longitudinal gap height.

    - ``gap_angle`` : ``float``
        Angle subtended by the gap arc from the flange center.

    - ``E`` : ``float`` [optional]
        Young modulus of the flange. If omitted, it will be taken equal to 210e9 Pa.

    - ``G`` : ``float`` [optional]
        Shear modulus of the flange. If omitted, it will be taken equal to 80.77e9 Pa.

    - ``s_ratio`` : ``float`` [optional]
        Ratio of bottom shell thickness over s. If omitted, it will be take equal to 1.0,
        threfore, by default, s_botom = s.

    The given parameters are also available as attributes (e.g. ``fseg.a``, ``fseg.Fv``, etc.).
    This class is designed to be immutable, therefore modifying the attributes after
    instantiation is not a good idea. If you need a segment with different attributes, just
    create a new one.
    '''

    a: float        # distance between inner face of the flange and center of the bolt hole
    b: float        # distance between center of the bolt hole and center-line of the shell
    s: float        # shell thickness
    t: float        # flange thickness
    c: float        # shell arc length
    R: float        # shell outer curvature radius

    Zg: float       # load applied to the flange segment shell at rest (normally dead weight
                    # of tower + RNA, divided by the number of bolts). Negative if compression.

    bolt: Bolt      # Bolt object representing the flange segment bolt
    Fv: float       # applied bolt preload

    Do: float       # Bolt hole diameter
    Dw: float       # Washer diameter

    gap_height: float   # maximum longitudinal gap height
    gap_angle: float    # angle subtended by the gap arc from the flange center

    E: float = 210e9    # Young modulus of the flange
    G: float = 80.77e9  # Shear modulus of the flange
    s_ratio: float = 1.0    # Ratio of bottom shell thickness over s. Default s_botom = s.


    #TODO: Verify failure mode B

    @cached_property
    def _bolt_axial_stiffness (self):
        return self.bolt.axial_stiffness(2*self.t)


    @cached_property
    def _bolt_bending_stiffness (self):
        return self.bolt.bending_stiffness(2*self.t)


    @cached_property
    def _flange_axial_stiffness (self):
        # Stiffnes of flange w.r.t. compression in thickness direction,
        # when no gap is present. Calculated according to ref. [3] and [4].
        from math import pi
        Dw = self.Dw
        Do = self.Do
        h = self.t * 2
        A = pi * ((Dw + h/10)**2 - Do**2) / 4
        return self.E * A / h


    def _bolt_moment (self, Z, Fs):
        a_red = self.b / (self._prying_lever_ratio - 1)
        a_star = max(0.5, min((self.t / (a_red + self.b))**2 , 1)) * a_red
        I_tg = self.c * self.t**3 / 12
        ak = self._stiffness_correction_factor
        bolt_rotation = Z*self.b*a_star / (3*self.E*I_tg*ak) + (Fs - self.Fv) / (2*a_star*self._bolt_axial_stiffness)
        return bolt_rotation * 2*self._bolt_bending_stiffness


    @cached_property
    def shell_force_at_rest (self):
        ''' Shell force when no external loads are applied

        The shell loads at rest are normally the self-weights of
        the structure supported by the flange.
        '''
        return self.Zg


    @cached_property
    def bolt_force_at_rest (self):
        ''' Bolt axial force when no external loads are applied

        The bolt force at rest is just the bolt pretension.
        '''
        return self.Fv


    @cached_property
    def bolt_moment_at_rest (self):
        Z1 = self.shell_force_at_rest
        Fs1 = self.bolt_force_at_rest
        return self._bolt_moment(Z1, Fs1)


    @cached_property
    def shell_force_at_small_displacement (self):
        ''' Intermediate shell pull, between rest and tensile failure

        This is an auxiliary point that gives the polynomial the right
        value of initial slope. It is evaluated according to ref. [1],
        sec.9.2.2.3.
        '''

        # Retrieve point 2A (called point 0 in [1]) and determine Z as
        # a low pecentage of the theoretical pull Z0.
        Z0 = self._ideal_shell_force_at_tensile_ULS
        return 0.05 * self._stiffness_correction_factor * Z0


    @cached_property
    def bolt_force_at_small_displacement (self):
        ''' Intermediate bolt pull, between rest and tensile failuse

        This is an auxiliary point that gives the polynomial the right
        value of initial slope. It is evaluated according to ref. [1],
        sec.9.2.2.3.
        '''

        # The slope between points P1 and P3 should match the
        # theoretical value of stiffness of the system.
        Z = self.shell_force_at_small_displacement
        return self.Fv + self._polynomial_initial_slope * (Z - self.Zg)


    @cached_property
    def bolt_moment_at_small_displacement (self):
        Z3 = self.shell_force_at_small_displacement
        Fs3 = self.bolt_force_at_small_displacement
        return self._bolt_moment(Z3, Fs3)


    @cached_property
    def shell_force_at_tensile_ULS (self):
        return self._stiffness_correction_factor * self._cantilever_shell_force_at_tensile_ULS


    @cached_property
    def bolt_force_at_tensile_ULS (self):
        ''' Bolt axial force at tensile failure

        Assuming the failure mode B, in the ULS, the bolt is subjected
        to its maximum tensile capacity.
        '''

        # The bolt is loaded with the ultimate capacity, by definition.
        # If the pretension Fv is too close to the ultimate capacity Fsu, the polynomial
        # function may get too steep, therefore we make sure that Fs2 is at list 125% of Fv.
        return max(self.bolt.ultimate_tensile_capacity(), 1.25*self.bolt_force_at_rest)


    @cached_property
    def bolt_moment_at_tensile_ULS (self):
        Z2 = self.shell_force_at_tensile_ULS
        Fs2 = self.bolt_force_at_tensile_ULS
        return self._bolt_moment(Z2, Fs2)


    @cached_property
    def shell_force_at_closed_gap (self):
        ''' Force necessary to completely close the imperfection gap '''
        return 0.5 * self._gap_stiffness * self.gap_height * self.c


    @cached_property
    def _ideal_shell_force_at_tensile_ULS (self):
        ''' Shell pull force at the theoretical state of full prying

        This property represents the shell pull forces when the flange segment
        is in tensile ULS and in the ideal situation of no gap.

        This variable is indicated as Z0 in ref. [1].
        '''

        return self.bolt_force_at_tensile_ULS / self._prying_lever_ratio


    @cached_property
    def _cantilever_shell_force_at_tensile_ULS (self):
        ''' Shekk pull force at full prying, after gap closing

        This property represents the shell pull force necessary to
        close the inner side of the gap and then keep pulling the
        bolt to it ultimate tensile limit.

        This value is calculated modelling the flange segment as a
        simple cantilever (neglecting the gap spring contribution).
        Ref. [1], variable Z2-tilde.
        '''

        # Shift the shell pull by the force necessary to close the gap.
        # If the gap closing force is too high, Z may become negative. In order to
        # avoid that, we limit the value of Z to 20% of Z0.
        Z0 = self._ideal_shell_force_at_tensile_ULS
        return max(
            Z0 - self.shell_force_at_closed_gap,
            0.2 * Z0)


    @cached_property
    def _prying_lever_ratio (self):
        ''' Lever ratio A, as defined in [9]'''

        # Ref. [9] uses different symbolts than ref. [1].
        # This getter uses the symbols defined in ref. [9].
        e = self.a
        g = self.b

        # The flange is considered rigid if e <= 1.25*g.
        # In a rigid flange, the pivid point is the edge, therefore e_reduced = e.
        if e/g <= 1.25:
            return (e + g) / e

        # For e > 2.25*g, the model defined in ref. [9] has not been
        # validated. A warning is thrown, but then the model is applied
        # anyways.
        if e/g > 2.25:
            logger.warning("Flange geometry out of validity range for Tobinaga & Ishihara lever ratio formulation: e/g > 2.25.")

        # Coefficient a, expressing the slenderness of the longitudinal
        # cross-section of this flange-segment as tatio between thickness
        # and length.
        a = min(self.t / (e+g), 1.0)
        if a < 0.55 - 0.12 * (e/g):
            # When outside the boundary of validations, throw a warning, but then
            # apply the model anyways.
            logger.warning("Flange geometry out of validity range for Tobinaga & Ishihara lever ratio formulation: a < 0.55 - 0.12 * (e/g).")

        # Evaluate the ratio between distance e (pivit point location for rigid body rotation)
        # and the acctual center of reaction at the prying contact location.
        b = (e/g - 1.25)**0.32 + 0.45
        actionpoint_correction_factor = min(1 - (1 - a**b)**5, 1.0)

        # Distance from the center of reaction at prying contact location, form
        # the center of bolt hole.
        e_reduced = actionpoint_correction_factor * e

        # Lever ratio
        return (e_reduced + g) / e_reduced


    @cached_property
    def _gap_stiffness (self):
        ''' Stiffness of the design gap.

        Returns the gap stiffnes as a spring constant per unit of flange-segment
        arc length. This is calculated according to ref.[1], sec.9.1.
        '''

        # Calculate the shell stiffness
        Rm = self.R - self.s/2   # radius of the shell midline
        L_gap = self.R * self.gap_angle
        k_fac = max(1.8, 1.3 + (8.0e-4 - 1.6e-7 * (Rm*1000)) * (L_gap*1000))    # ref. [1], eq.48
        s_avg = (self.s + self.s_ratio * self.s) / 2
        k_shell = self.E * s_avg / (k_fac * L_gap)                   # ref. [1], eq.47
        logger.debug(f"k_fac = {k_fac} ")
        logger.debug(f"k_shell_ini = {k_shell/1e6:.2f} kN/mm/m")

        # Calculate the flange stiffness
        w = self.a + self.b + self.s/2      # flange segment length
        A = w * self.t                      # flange segment longitudinal cross-section area
        I = w * self.t**3 / 12              # flange segment longitudinal corss-section second moment of area
        EI = self.E * I
        GA = self.G * A
        L2 = L_gap**2
        k_flange = 384 * EI * GA / (L2 * (GA*L2 + 48*EI))   # ref. [1], eq.49
        logger.debug(f"A_cf = {A*1e6:.2f} mm^2")
        logger.debug(f"I_cf = {I*1e12:.2f} mm^4")
        logger.debug(f"k_fl = {k_flange/1e6:.2f} kN/mm/m")

        # Total gap stiffness according to ref. [1], eq.53
        return 2.2 * (k_shell + k_flange)


    @cached_property
    def _stiffness_correction_factor (self):
        ''' Stiggness corrections factor.

        This factor, modifies the segment force to accorunt for the
        effect of the gap spring. It is evaluate according to ref. [1],
        sec.9.2.2.2, where it goes by the symbol alpha-k.
        '''
        logger.debug("STIFFNESS CORRECTION FACTOR CALCULATION:")

        from math import pi

        # Retrieve point 2B
        Z2B = self._cantilever_shell_force_at_tensile_ULS
        Fs0 = self.bolt_force_at_tensile_ULS

        # Evaluate the displacement u in the ultimate prying state.
        a_red = self.b / (self._prying_lever_ratio - 1)
        w = self.a + self.b + self.s/2
        I = w * self.t**3 / 12
        u = (Z2B * self.b**2 / (3 * self.E * I) + (Fs0 - self.Fv) / (2 * self._bolt_axial_stiffness * a_red)) * (a_red + self.b)   # ref. [1], eq.72
        logger.debug(f"u = {u*1000:.3f} mm")

        # Evaluate the segment stiffness
        k_seg = Z2B / (u * self.c)
        logger.debug(f"k_seg = {k_seg/1e6} kN/mm/m")

        # Return the stiffness correction factor, acc. [1], eq.75
        return min(1 + self._gap_stiffness / k_seg,
                   4 * pi/3 / self.gap_angle)


    @cached_property
    def _polynomial_initial_slope (self):
        ''' Initial slope of the polynomial Fs(Z).

        This slope is calculated according to ref. [1], eq.80.
        '''

        # Load factor of the tension spring
        p = self._bolt_axial_stiffness / (self._bolt_axial_stiffness + self._flange_axial_stiffness)

        # Initial slope correction factor
        scf = min(1.0 , (self.shell_force_at_closed_gap / (0.2 * self.Fv))**2)

        # Initial slope
        return scf * p
