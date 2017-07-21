#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''SrFit example for a simple linear fit to a noisy data.

This script can be run in IPython "demo" mode.  To use the demo mode,
start IPython and execute the following commands:

In [1]: %run ex03.py demo
In [2]: demo()
...
In [3]: demo()
...
'''

# Define "demo" object and exit if run with a single argument "demo".
from __future__ import print_function
import sys
if __name__ == '__main__' and sys.argv[1:] == ['demo']:
    from IPython.lib.demo import ClearDemo
    demo = ClearDemo(__file__)
    demo.seek(1)
    print('Created "demo" object.  Use "demo()" to run the next section.')
    sys.exit()

# <demo> auto_all
# <demo> silent
# <demo> --- stop ---

# Simulate linear data with some random Gaussian noise.

import numpy as np
xobs = np.arange(-10, 10.1)
dyobs = 0.3 * np.ones_like(xobs)
yobs = 0.5 * xobs + 3 + dyobs * np.random.randn(xobs.size)

# Plot the generated "observed" data (xobs, yobs).

import matplotlib.pyplot as plt
plt.ion(); plt.clf(); plt.hold(False)
plt.plot(xobs, yobs, 'x')
plt.title('y = 0.5*x + 3 generated with a normal noise at sigma=0.3')
plt.show()

# <demo> --- stop ---

# We are going to define a line fitting regression using SrFit.
# At first we create a SrFit Profile object that holds the observed data.

from diffpy.srfit.fitbase import Profile
linedata = Profile()
linedata.setObservedProfile(xobs, yobs, dyobs)

# The second step is to create a FitContribution object, which associates
# observed profile with a mathematical model for the dependent variable.

from diffpy.srfit.fitbase import FitContribution
linefit = FitContribution('linefit')
linefit.setProfile(linedata)
linefit.setEquation("A * x + B")

# SrFit objects can be examined by calling their show() function.  SrFit
# parses the model equation and finds two parameters A, B at independent
# variable x.  The values of parameters A, B are at this stage undefined.

linefit.show()

# <demo> --- stop ---

# We can set A and B to some specific values and calculate model
# observations.  The x and y attributes of the FitContribution are
# the observed values, which may be re-sampled or truncated to a shorter
# fitting range.

linefit.A
linefit.A = 3
linefit.B = 5
print(linefit.A, linefit.A.value)
print(linefit.B, linefit.B.value)

# <demo> --- stop ---

# linefit.evaluate() returns the modeled values and linefit.residual
# the difference between observed and modeled data scaled by estimated
# standard deviations.

print("linefit.evaluate() =", linefit.evaluate())
print("linefit.residual() =", linefit.residual())
plt.plot(xobs, yobs, 'x', linedata.x, linefit.evaluate(), '-')
plt.title('Line simulated at A=3, B=5')

# <demo> --- stop ---

# We want to find optimum model parameters that fit the simulated curve
# to the observations.  This is done by associating FitContribution with
# a FitRecipe object.  FitRecipe can manage multiple fit contributions and
# optimize all models to fit their respective profiles.

from diffpy.srfit.fitbase import FitRecipe
rec = FitRecipe()
# clearFitHooks suppresses printout of iteration number
rec.clearFitHooks()

rec.addContribution(linefit)
rec.show()


# <demo> --- stop ---

# FitContributions may have many parameters.  We need to tell the recipe
# which of them should be tuned by the fit.

rec.addVar(rec.linefit.A)
rec.addVar(rec.linefit.B)

# The addVar function created two attributes A, B for the rec object
# which link ot the A and B parameters of the linefit contribution.

print("rec.A =", rec.A)
print("rec.A.value =", rec.A.value)

# The names of the declared variables are stored in a rec.names
# and the corresponding values in rec.values.

print("rec.values =", rec.values)
print("rec.names =", rec.names)

# Finally the recipe objects provides a residual() function to calculate
# the difference between the observed and simulated values.  The residual
# function can accept a list of new variable values in the same order as
# rec.names.

print("rec.residual() =", rec.residual())
print("rec.residual([2, 4]) =", rec.residual([2, 4]))

# <demo> --- stop ---

# The FitRecipe.residual function can be directly used with the scipy
# leastsq function for minimizing a sum of squares.

from scipy.optimize import leastsq
leastsq(rec.residual, rec.values)

# Recipe variables and the linked line-function parameters are set to the
# new optimized values.

print(rec.names, "-->", rec.values)
linefit.show()

# The calculated function is available in the ycalc attribute of the profile.
# It can be also accessed from the "linefit" contribution attribute of the
# recipe as "rec.linefit.profile.ycalc".
plt.plot(linedata.x, linedata.y, 'x', linedata.x, linedata.ycalc, '-')
plt.title('Line fit using the leastsq least-squares optimizer')

# <demo> --- stop ---

# The FitRecipe.scalarResidual function returns the sum of squares and can
# be used with a minimizer that expects scalar function:

from scipy.optimize import fmin
fmin(rec.scalarResidual, [1, 1])
print(rec.names, "-->", rec.values)
plt.plot(linedata.x, linedata.y, 'x', linedata.x, linedata.ycalc, '-')
plt.title('Line fit using the fmin scalar optimizer')

# <demo> --- stop ---

# For a converged fit recipe, the details of the fit can be extracted
# with the FitResults class.

from diffpy.srfit.fitbase import FitResults
res = FitResults(rec)
print(res)

# <demo> --- stop ---

# Variables defined in the recipe can be fixed to a constant value.

rec.fix(B=0)

# The fixed variables can be checked using the "fixednames" and
# "fixedvalues" attributes of a recipe.
print("free:", rec.names, "-->", rec.names)
print("fixed:", rec.fixednames, "-->", rec.fixedvalues)

# The fit can be rerun with a constant variable B.
leastsq(rec.residual, rec.values)
print(FitResults(rec))
plt.plot(linedata.x, linedata.y, 'x', linedata.x, linedata.ycalc, '-')
plt.title('Line fit for variable B fixed to B=0')

# <demo> --- stop ---

# Fixed variables may be released with the "free" function.
# free("all") releases all fixed variables.
rec.free('all')

# Variables may be constrained to a result of an expression.
rec.constrain(rec.A, "2 * B")

# Perform linear fit where slope is twice the offset.
leastsq(rec.residual, rec.values)
print(FitResults(rec))
plt.plot(linedata.x, linedata.y, 'x', linedata.x, linedata.ycalc, '-')
plt.title('Line fit for variable A constrained to A = 2*B')

# <demo> --- stop ---

# Constraint expressions can be removed by calling the unconstrain function.
rec.unconstrain(rec.A)

# Variables may be restrained to a specific range.  Here "ub" is the upper
# boundary and "sig" acts as a standard deviation for ((x - ub)/sig)**2
# penalty function.

arst = rec.restrain(rec.A, ub=0.2, sig=0.001)

# Perform fit with the line slope restrained to a maximum value of 0.2:
leastsq(rec.residual, rec.values)
print(FitResults(rec))
plt.plot(linedata.x, linedata.y, 'x', linedata.x, linedata.ycalc, '-')
plt.title('Line fit with A restrained to an upper bound of 0.2')
