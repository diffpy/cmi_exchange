#!/usr/bin/env python

"""Demonstrate user-defined profile function for PDF calculation.
"""

from diffpy.srreal.peakprofile import PeakProfile


class RectangleProfile(PeakProfile):
    """Rectangle profile function with a unit area.
    """

    # overload functions from the base class

    def __call__(self, x, fwhm):
        """Evaluate rectangle function centered at zero.

        x    -- independent variable to calculate the profile at
        fwhm -- width of the rectangle profile.  In PDF simulation
                this is determined from displacement parameters of
                each contributing pair of atoms.

        Return the profile function at x.
        """
        y = 0.0
        if -fwhm/2.0 < x < +fwhm/2.0:
            y = 1.0 / fwhm
        return y


    def clone(self):
        "Return a copy of this profile object."
        import copy
        return copy.copy(self)


    def create(self):
        "Return new instance of this profile type."
        return RectangleProfile()


    def type(self):
        "Return unique string identifier for this profile type."
        return "rectangleprofile"


    def xboundhi(self, fwhm):
        """Upper bound where profile becomes smaller than the requested
        precision (self.precision)."""
        return +0.5 * fwhm


    def xboundlo(self, fwhm):
        """Lower bound where profile becomes smaller than the requested
        precision (self.precision)."""
        return -0.5 * fwhm

# end of class RectangleProfile

# Register this profile function so it can be assigned by its string type.
RectangleProfile()._registerThisType()
