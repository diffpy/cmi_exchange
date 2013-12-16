#!/usr/bin/env python
########################################################################
#
# srfit-demos       Complex Modeling Initiative
#                   Pavol Juhas
#                   (c) 2013 Brookhaven National Laboratory,
#                   Upton, New York.  All rights reserved.
#
# File coded by:    Xiahao Yang, Kevin Knox
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
########################################################################

"""IPython extension for SrFit fit of Gaussian peak to user data.

This is an example of defining a Gaussian peak fit using SrFit and
its sharing as IPython extension.

Usage in IPython shell:

Install this extension with

    %install_ext https://raw.github.com/diffpy/srfit-demos/master/gaussianfit.py

Activate this extension using

    %load_ext gaussianfit

or adjust the c.InteractiveShellApp.extensions variable in ipython_config.py
to load it at startup every time.


To try out the class execute the following commands:

    import numpy as np
    x = linspace(-10, 10, 100)
    A, x0, sig = 5, -2.5, 1.2
    y = A * np.exp(-0.5*(x-x0)**2/sig**2) + np.random.normal(0, 0.2, 100)
    gfit = GaussianFit(x, y)
    gfit.refine()
    gfit.plot()

    x, y, dy are the data to be fitted with Gaussian peak (dy may be omitted)
    A, sig, and x0 are initial values.  If omitted the program will estimate
    their starting values.

This extension is based on the SrFit example gaussianrecipe.py
"""

from diffpy.srfit.fitbase import FitContribution, FitRecipe, Profile, FitResults
import numpy as np

class GaussianFit(object):
    '''Data attributes:

    Input data:

    x    --  input x values (read only)
    y    --  input y values (read only)
    dy   --  input dy values (read only)

    Calculated parameters:

    A    --  area under curve
    sig  --  width of curve
    x0   --  x-position of center of curve
    yg   --  gaussian function calculated for the current A, sig, x0

    import numpy as np
    x = linspace(-10, 10, 100)
    A, x0, sig = 5, -2.5, 1.2
    y = A * np.exp(-0.5*(x-x0)**2/sig**2) + np.random.normal(0, 0.2, 100)
    gfit = GaussianFit(x, y)
    gfit.refine()
    gfit.plot()

    x, y, dy are the data to be fitted with Gaussian peak (dy may be omitted)
    A, sig, and x0 are initial values.  If omitted the program will estimate
    their starting values.
   '''

    def __init__(self, x, y, dy=None, A=None, sig=None, x0=None):
        '''Create new GaussianFit object
        '''
        self._x = x
        self._y = y
        self._dy = np.ones_like(x) if dy is None else dy

        if (A is None) or (sig is None) or (x0 is None):
            self._getStartingValues()
        else:
            self._A = A
            self._sig = sig
            self._x0 = x0

        self._makeRecipe()
        self._yg = None
        print 'Starting values for parameters:'
        self.printValues()

        return

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def dy(self):
        return self._dy

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value):
        self._A = value
        self._recipe.A.value = value

    @property
    def sig(self):
        return self._sig

    @sig.setter
    def sig(self, value):
        self._sig = value
        self._recipe.sig.value = value

    @property
    def x0(self):
        return self._x0

    @x0.setter
    def x0(self, value):
        self._x0 = value
        self._recipe.x0.value = value

    @property
    def yg(self):
        return self._yg

    def _getStartingValues(self):
        '''Estimate starting values for A, sig, and x0
        '''
        peakValue = np.max(self._y)
        peakIndex = np.argmax(self._y)
        self._x0 = self._x[peakIndex]
        self._sig = (self._y > peakValue/2).sum() * np.abs((self._x[1]-self._x[0])) / 2.5
        self._A = peakValue * self._sig

    def _makeRecipe(self):
        '''Make a FitRecipe for fitting a Gaussian curve to data.
        '''
        profile = Profile()
        profile.setObservedProfile(self._x, self._y, self._dy)

        contribution = FitContribution("g1")
        contribution.setProfile(profile, xname="x")
        contribution.setEquation("A * exp(-0.5*(x-x0)**2/sig**2)")

        recipe = FitRecipe()
        recipe.addContribution(contribution)
        recipe.addVar(contribution.A, self._A)
        recipe.addVar(contribution.x0, self._x0)
        recipe.addVar(contribution.sig, self._sig)

        self._recipe = recipe
        return

    def printValues(self):
        '''Print out values of Gaussian parameters
        '''
        print 'A = ', self._A
        print 'sig = ', self._sig
        print 'x0 = ', self._x0

    def plot(self):
        '''Plot the input data and the best fit.
        '''
        import pylab
        pylab.figure()
        pylab.plot(self._x, self._y, 'b.', label="observed Gaussian")
        if self._yg is not None: pylab.plot(self._x, self._yg, 'g-', label="calculated Gaussian")
        pylab.legend(loc=(0.0, 0.8))
        pylab.xlabel("x")
        pylab.ylabel("y")
        pylab.show()
        return

    def refine(self):
        '''Optimize the recipe created above using scipy.
        '''
        from scipy.optimize.minpack import leastsq
        print "Fit using scipy's LM optimizer"
        leastsq(self._recipe.residual, self._recipe.getValues())
        self._A, self._x0, self._sig = self._recipe.getValues()
        self._yg = self._recipe.g1.profile.ycalc
        print 'Refined parameter values:'
        self.printValues()
        return

# end of class GaussianFit

def load_ipython_extension(ip):
    ip.user_ns['GaussianFit'] = GaussianFit
    return
