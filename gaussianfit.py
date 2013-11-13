#!/usr/bin/env python
########################################################################
#
# diffpy.srfit      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2009 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chris Farrow
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
########################################################################
"""Example of ipython extension of fitting a Gaussian to simulated data.

This is an example simply shows how to write an ipython extension for SrFit 

Use:
    %install_ext https://raw.github.com/diffpy/srfit-demos/master/gaussianfit.py
    
Once to install, and then
    %load_ext gaussianfit
    
To fit the data, run
    gaussianfit(x, y, dy, A, sig, x0)
    
    x, y, dy are gaussian date to be fitted, A, sig, x0 are initial value,
    
This extension is based on srfit example gaussianrecipe.py 
"""

from diffpy.srfit.fitbase import FitContribution, FitRecipe, Profile, FitResults
import numpy as np

####### Example Code

def makeRecipe(x, y, dy, A, sig, x0):
    """Make a FitRecipe for fitting a Gaussian curve to data.    
    """
    profile = Profile()
    profile.setObservedProfile(x, y, dy)

    contribution = FitContribution("g1")
    contribution.setProfile(profile, xname="x")
    contribution.setEquation("A * exp(-0.5*(x-x0)**2/sigma**2)")

    recipe = FitRecipe()
    recipe.addContribution(contribution)
    recipe.addVar(contribution.A, A)
    recipe.addVar(contribution.x0, x0)
    recipe.addVar(contribution.sigma, sig)
    return recipe

def scipyOptimize(recipe):
    """Optimize the recipe created above using scipy.
    """
    from scipy.optimize.minpack import leastsq
    print "Fit using scipy's LM optimizer"
    leastsq(recipe.residual, recipe.getValues())
    
    return

def plotResults(recipe):
    """Plot the results contained within a refined FitRecipe."""
    x = recipe.g1.profile.x
    y = recipe.g1.profile.y
    ycalc = recipe.g1.profile.ycalc

    # This stuff is specific to pylab from the matplotlib distribution.
    import pylab
    pylab.plot(x, y, 'b.', label = "observed Gaussian")
    pylab.plot(x, ycalc, 'g-', label = "calculated Gaussian")
    pylab.legend(loc = (0.0,0.8))
    pylab.xlabel("x")
    pylab.ylabel("y")

    pylab.show()
    return

def gaussianfit(x, y, dy=None, A=1.0, sig=1.0, x0=0.0):
#def gaussianfit(arg):
    '''main function to fit and plot gaussian curve
        x, y, dy:   gaussian date to be fitted 
        A, sig, x0: initial value
    '''
    #print type(arg)
    dy = np.ones_like(x) if dy==None else dy
    
    recipe = makeRecipe(x, y, dy, A, sig, x0)
    scipyOptimize(recipe)
    res = FitResults(recipe)
    res.printResults()
    plotResults(recipe)
    return 

def load_ipython_extension(ip):
    ip.user_ns['gaussianfit']=gaussianfit
    return

if __name__ == "__main__":
    x,y,dy = np.loadtxt("gau.dat").T
    gaussianfit(x,y)

# End of file