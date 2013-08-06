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
import sys
if __name__ == '__main__' and sys.argv[1:] == ['demo']:
    from IPython.lib.demo import ClearDemo
    demo = ClearDemo(__file__)
    demo.seek(1)
    print 'Created "demo" object.  Use "demo()" to run the next section.'
    sys.exit()

# <demo> silent
# <demo> --- stop ---

xobs = np.arange(-10, 10.1)
yobs = 0.5 * xobs + 3 + 0.3 * np.random.randn(xobs.size)
clf()
plot(xobs, yobs, 'x')
show()

# <demo> --- stop ---

# We are going to define a line fitting regression using srfit.
# At first we create a srfit Profile object that holds the observed data.

from diffpy.srfit.fitbase import Profile
linedata = Profile()
linedata.setObservedProfile(xobs, yobs)
# <demo> --- stop ---

# The second step is to create FitContribution object, which associates
# observed profile with a mathematical model for the dependent variable.

from diffpy.srfit.fitbase import FitContribution
linefit = FitContribution('linefit')
linefit.setProfile(linedata)
linefit.setEquation("A * x + B")
# <demo> --- stop ---
# <demo> auto

# srfit objects can be examined by calling their show() function.
# SrFit parses the model equation and finds two parameters A, B.
# Their values are at this stage undefined.

linefit.show()
# <demo> --- stop ---

# We can set A and B to some specific values and calculate model
# observations.  The x and y attributes of the FitContribution are
# the observed values, which can be resampled or truncated to a shorter
# fitting range.

linefit.A
linefit.A = 3
linefit.B = 5
linefit.evaluate()

# <demo> auto

# We want to find optimum model parameters that fit the simulated curve
# to the observations.  This is done by associating FitContribution with
# a FitRecipe object.  FitRecipe can manage multiple fit contributions and
# optimize all models to fit their respective profiles.

from diffpy.srfit.fitbase import FitRecipe
rec = FitRecipe()
rec.addContribution(linefit)
rec.show()

# <demo> --- stop ---

# FitContributions may have many parameters.  We need to tell the recipe
# object which of them should be tuned by the fit.

rec.addVar(rec.linefit.A)
rec.addVar(rec.linefit.B)
rec.show()

# <demo> auto

# The addVar function created two attributes A, B for the rec object
# which link ot the A and B parameters of the linefit contribution.

print rec.A, rec.A.value

# The names of the declared variables are stored in a rec.names
# and the corresponding values in rec.values.

print "rec.values =", rec.values
print "rec.names =", rec.names

# Finally the recipe objects provides a residual() function to calculate
# the difference between the observed and simulated values.  The residual
# function can accept a list of new variable values in the same order as
# rec.names.

print "rec.residual() =", rec.residual()
print "rec.residual([2, 4]) =", rec.residual([2, 4])

# <demo> --- stop ---

# The FitRecipe.residual function can be directly used with the scipy
# leastsq function for minimizing a sum of squares.

from scipy.optimize import leastsq
leastsq(rec.residual, rec.values)

# <demo> --- stop ---

# The FitRecipe.scalarResidual function returns the sum of squares and can
# be used with a minimizer that expects scalar function:

from scipy.optimize import fmin
fmin(rec.scalarResidual, [1, 1])
plot(linedata.x, linedata.ycalc)

# <demo> --- stop ---

# For a converged fit recipe, the details of the fit can be obtained
# using the FitResults class.

from diffpy.srfit.fitbase import FitResults
res = FitResults(rec)
print res

# <demo> --- stop ---

# FIXME below
DISABLE = '''
# FitRecipe can be use to fix 
res=FitResults(rec)
print res
rec.fix(B=0)
rec.show()
rec.names
rec.fixednames
rec.fixedvalues
from scipy.optimize import leastsq
leastsq(rec.residual, rec.values)
rec.values
plot(xobs, linefit.evaluate())

rec.constrain(rec.A, "2 * B")
rec.names
rec.fixednames
rec.free('B')
rec.names
rec.values
leastsq(rec.residual, rec.values)
plot(xobs, linefit.evaluate())
print FitResults(rec)
rec.show()
get_ipython().magic(u'pinfo rec.unconstrain')
rec.unconstrain('A')
rec.names
rec.values
get_ipython().magic(u'pinfo rec.restrain')
ares=rec.restrain('A', ub=0.4)
ares
ares.sig
ares.scaled
leastsq(rec.residual, rec.values)
ares.scaled
ares.scaled=True
leastsq(rec.residual, rec.values)
ares.sig=0.01
leastsq(rec.residual, rec.values)
ares.scaled=False
leastsq(rec.residual, rec.values)
plot(xobs, linefit.evaluate())
rec
from cPickle
from cPickle import dumps
s=dumps(rec)
from pickle import dumps
s=dumps(rec)
get_ipython().magic(u'save ex03.py 1-127')
'''
