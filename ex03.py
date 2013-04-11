# coding: utf-8
figure()
close()
xobs=arange(-10, 10.1)
xobs
get_ipython().magic(u'pinfo randn')
yobs=0.5*xobs + 3 + 0.3 * randn(21)
plot(xobs, yobs, 'x')
from diffpy.srfit.fitbase import Profile
help(Profile)
get_ipython().magic(u'hist')
linedata=Profile()
get_ipython().magic(u'pinfo linedata.setObservedProfile')
linedata.setObservedProfile(xobs, yobs)
from diffpy.srfit.fitbase import FitContribution
help(FitContribution)
linefit=FitContribution('linefit')
linefit.setProfile(linedata)
help(linefit.setEquation)
linefit.show()
linefit.setEquation("A * x + B")
linefit.show()
linefit.A
linefit.A=3
linefit.B=5
linefit.evaluate()
linefit.show()
linefit.y
linefit.profile
linefit.x.value
linefit.x
linefit.x.value
linefit.profile
linedata
clf()
plot(linedata.x, linedata.yobs)
plot(linedata.x, linedata.ycalc)
linedata.ycalc)
linedata.ycalc
linedata.y
linedata.yobs
plot(xobs, linefit.evaluate())
get_ipython().magic(u'pinfo linefit.evaluate')
linefit.show()
linefit.A=-0.5
plot(xobs, linefit.evaluate())
from diffpy.srfit.fitbase import FitRecipe
help(FitRecipe)
rec=FitRecipe()
help(rec.addContribution)
rec.addContribution(linefit)
rec.show()
rec.linefit
rec.linefit.A
rec.linefit.A.value
from scipy.optimize import fmin
help(fmin)
get_ipython().magic(u'pinfo rec.addVar')
rec.addVar(rec.linefit.A)
rec.A
rec.A.value
rec.addVar(rec.linefit.B)
rec.show()
rec.names
rec.values
rec.residual()
get_ipython().magic(u'pinfo rec.residual')
rec.names
rec.values
rec.residual([1, 2])
rec.show()
rec.scalarResidual()
get_ipython().magic(u'pinfo fmin')
fmin(rec.scalarResidual, rec.values)
clf()
plot(xobs, yobs, '.')
plot(xobs, linefit.evaluate())
from diffpy.srfit.fitbase import FitResults
get_ipython().magic(u'pinfo FitResults')
help(FitResults)
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