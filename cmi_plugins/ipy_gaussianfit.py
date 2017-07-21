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

Activate this extension using

    %load_ext cmi_plugins.ipy_gaussianfit

or adjust the c.InteractiveShellApp.extensions variable in ipython_config.py
to load it at startup every time.


To try out the class execute the following commands:

import numpy as np
x = np.arange(-10, 10, 0.1)
x0, sig = -2, 1.5
noise = 0.2 * np.ones_like(x)
y = np.exp(-0.5*(x-x0)**2/sig**2) + noise * np.random.randn(*x.shape)
gfit = GaussianFit(x, y, noise)
gfit.refine()
gfit.plot()

x, y, dy are the data to be fitted with Gaussian peak (dy may be omitted)
A, sig, and x0 are initial values.  If omitted the program will estimate
their starting values.

This extension is based on the SrFit example gaussianrecipe.py
"""

from diffpy.srfit.fitbase import FitContribution, FitRecipe, Profile, FitResults


class GaussianFit(object):
    '''Least-squares fit of Gauss function to the specified data.

    Input and simulated data (read-only):

    x    --  input x values
    y    --  input y values
    dy   --  estimated standard deviations for the y-values
    yg   --  Gauss function calculated for the current A, sig, x0

    Parameters of the Gauss function:

    A    --  integrated area of the fitted peak
    sig  --  width of curve (parameter sigma in the Gauss distribution
             function)
    x0   --  x-position of the peak center

    Fit-related objects:

    results -- result report from the last refinement, refined values,
             and their estimated errors, parameter correlations, etc.
    recipe -- FitRecipe from SrFit that manages this refinement
    '''

    def __init__(self, x, y, dy=None, A=None, sig=None, x0=None):
        '''Create new GaussianFit object

        x, y -- curve to be fitted with Gaussian peak.
        dy   -- estimated standard deviations for the y-values
                (may be omitted).
        A, sig, x0   -- optional initial parameters for the Gauss function.
                Omitted parameters will be estimated from the input data.
        '''
        self.results = None
        self._makeRecipe(x, y, dy)
        if None in (A, sig, x0):
            self._getStartingValues()
        if A is not None:  self.A = A
        if sig is not None:  self.sig = sig
        if x0 is not None:  self.x0 = x0
        print 'Initial parameter values:'
        self.printValues()
        return

    @property
    def x(self):
        return self.recipe.g1.profile.x

    @property
    def y(self):
        return self.recipe.g1.profile.y

    @property
    def dy(self):
        return self.recipe.g1.profile.dy

    @property
    def A(self):
        return self.recipe.A.value

    @A.setter
    def A(self, value):
        self.recipe.A = value
        return

    @property
    def sig(self):
        return self.recipe.sig.value

    @sig.setter
    def sig(self, value):
        self.recipe.sig = value
        return

    @property
    def x0(self):
        return self.recipe.x0.value

    @x0.setter
    def x0(self, value):
        self.recipe.x0 = value
        return

    @property
    def yg(self):
        return self.recipe.g1.evaluate()

    def _getStartingValues(self):
        '''Estimate starting values for A, sig, and x0
        '''
        from numpy import sqrt, log, pi
        x, y = self.x, self.y
        peakIndex = y.argmax()
        peakValue = y[peakIndex]
        self.x0 = x[peakIndex]
        halfmaxlo = (y < peakValue/2) & (x < self.x0)
        xhalflo = x[halfmaxlo][-1] if halfmaxlo.any() else x.min()
        halfmaxhi = (y < peakValue/2) & (x > self.x0)
        xhalfhi = x[halfmaxhi][0] if halfmaxhi.any() else x.max()
        fwhm = xhalfhi - xhalflo
        self.sig = fwhm / (2 * sqrt(2 * log(2)))
        self.A = peakValue * sqrt(2 * pi) * self.sig
        return


    def _makeRecipe(self, x, y, dy):
        '''Make a FitRecipe for fitting a Gaussian curve to data.
        '''
        profile = Profile()
        profile.setObservedProfile(x, y, dy)
        contribution = FitContribution("g1")
        contribution.setProfile(profile, xname="x")
        contribution.registerStringFunction(
                '1/sqrt(2 * pi * sig**2)', name='gaussnorm')
        contribution.setEquation(
                "A * gaussnorm * exp(-0.5 * (x - x0)**2/sig**2)")
        recipe = FitRecipe()
        recipe.addContribution(contribution)
        recipe.addVar(contribution.A)
        recipe.addVar(contribution.x0)
        recipe.addVar(contribution.sig)
        recipe.clearFitHooks()
        self.recipe = recipe
        return


    def printValues(self):
        '''Print out values of Gaussian parameters
        '''
        print 'A =', self.A
        print 'sig =', self.sig
        print 'x0 =', self.x0
        return


    def plot(self):
        '''Plot the input data and the best fit.
        '''
        import matplotlib.pyplot as plt
        plt.plot(self.x, self.y, 'b.', label="observed Gaussian")
        plt.plot(self.x, self.yg, 'g-', label="calculated Gaussian")
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
        return


    def refine(self):
        '''Optimize the recipe created above using scipy.
        '''
        from scipy.optimize.minpack import leastsq
        leastsq(self.recipe.residual, self.recipe.values)
        self.results = FitResults(self.recipe)
        print "Fit results:\n"
        print self.results
        return

# end of class GaussianFit


def fitGaussian(x, y, dy=None, A=None, sig=None, x0=None):
    '''Fit Gaussian curve to the data and return calculated profile.

    x    -- input x values
    y    -- input y values
    dy   -- estimated standard deviations for the y-values (optional)
    A, sig, x0 -- optional initial parameters for the area, width and
            center of the Gauss function.  Omitted parameters will be
            estimated from the input data.

    Return a tuple of (yg, fit), where yg is the calculated Gaussian
    and fit and instance of the GaussianFit class with any details
    of the fit one could possible desire.
    '''
    fit = GaussianFit(x, y, dy=dy, A=A, sig=sig, x0=x0)
    fit.refine()
    return (fit.yg.copy(), fit)


def load_ipython_extension(ip):
    ip.user_ns['GaussianFit'] = GaussianFit
    ip.user_ns['fitGaussian'] = fitGaussian
    return
