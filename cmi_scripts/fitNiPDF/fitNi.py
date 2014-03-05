#!/usr/bin/env python
# -*- coding: utf-8 -*-


# We'll need numpy and pylab for plotting our results
import numpy as np
import pylab

# A least squares fitting algorithm from scipy
from scipy.optimize.minpack import leastsq

# DiffPy-CMI modules for building a fitting recipe 
from diffpy.Structure import loadStructure
from diffpy.srfit.pdf import PDFContribution
from diffpy.srfit.fitbase import FitRecipe 

# Files containing our experimental data and structure file
dataFile = "ni-q27r100-neutron.gr"
structureFile = "ni.cif"

# The first thing to construct is a contribution. Since this is a simple
# example, the contribution will simply contain our PDF data and an associated
# structure file. We'll give it the name "nickel"
niPDF = PDFContribution("nickel")

# Load the data and set the r-range over which we'll fit
niPDF.loadData(dataFile)
niPDF.setCalculationRange(xmin = 1, xmax = 20, dx = 0.01)

# Add the structure from our cif file to the contribution
niStructure = loadStructure(structureFile)
niPDF.addStructure("nickel", niStructure)
  
# The FitRecipe does the work of calculating the PDF with the fit variable
# that we give it.
niFit = FitRecipe()

# give the PDFContribution to the FitRecipe
niFit.addContribution(niPDF)

# Configure the fit variables and give them to the recipe.  We can use the
# srfit function constrainAsSpaceGroup to constrain the lattice and ADP
# parameters according to the Fm-3m space group.
from diffpy.srfit.structure import constrainAsSpaceGroup
spaceGroupParams = constrainAsSpaceGroup(niPDF.nickel.phase, "Fm-3m")

# We can now cycle through the parameters and add them to the recipe as
# variables
for par in spaceGroupParams.latpars:
    niFit.addVar(par)
for par in spaceGroupParams.adppars:
    niFit.addVar(par, 0.005)

# As usual, we add variables for the overall scale of the PDF and a delta2
# parameter for correlated motion of neighboring atoms.
niFit.addVar(niPDF.scale, 1)
niFit.addVar(niPDF.nickel.delta2, 5)

# We fix Qdamp based on prior information about our beamline.
niFit.addVar(niPDF.qdamp, 0.03, fixed = True)

# We can now execute the fit using scipy's least square optimizer.
print "Fit using scipy's LM optimizer"
leastsq(niFit.residual, niFit.getValues())


"""Now that the fit is done we can plot our results"""

# Get the experimental data from the recipe
r = niFit.nickel.profile.x
g = niFit.nickel.profile.y

# Get the calculated PDF and compute the difference between the calculated and
# measured PDF
gcalc = niFit.nickel.profile.ycalc
diffzero = -0.8 * max(g) * np.ones_like(g)
diff = g - gcalc + diffzero

# Plot!
pylab.figure()
pylab.plot(r,g,'bo',label="G(r) Data")
pylab.plot(r, gcalc,'r-',label="G(r) Fit")
pylab.plot(r,diff,'g-',label="G(r) diff")
pylab.plot(r,diffzero,'k-')
pylab.xlabel("$r (\AA)$")
pylab.ylabel("$G (\AA^{-2})$")
pylab.legend(loc=1)

pylab.show()

