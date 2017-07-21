#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This example will show how to perform mPDF refinements after performing the atomic
PDF refinement in SrFit. We use data from MnO at 15 K.
'''

# Import necessary functions
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

from diffpy.mpdf import *
from diffpy.Structure import loadStructure
from diffpy.srfit.pdf import PDFContribution
from diffpy.srfit.fitbase import FitRecipe, FitResults


# Files containing our experimental data and structure file
dataFile = "npdf_07334.gr"
structureFile = "MnO_R-3m.cif"
spaceGroup = "H-3m"
mnostructure = loadStructure(structureFile)

# Create the Mn2+ magnetic species
mn2p = MagSpecies(struc=mnostructure, label='Mn2+', magIdxs=[0,1,2],
                 basisvecs=2.5*np.array([[1,0,0]]), kvecs=np.array([[0,0,1.5]]),
                 ffparamkey='Mn2')

# Create and prep the magnetic structure
mstr = MagStructure()
mstr.loadSpecies(mn2p)
mstr.makeAll()

# Set up the mPDF calculator
mc = MPDFcalculator(magstruc=mstr, gaussPeakWidth=0.2)

### DO THE STRUCTURAL FIT USING SRFIT

# Construct the atomic PDF contribution
MnOPDF = PDFContribution("MnO")

# Load the data and set the r-range over which we'll fit
MnOPDF.loadData(dataFile)
MnOPDF.setCalculationRange(xmin=0.01, xmax=20, dx=0.01)

# Add the structure from our cif file to the contribution
MnOPDF.addStructure("MnO", mnostructure)

# The FitRecipe does the work of calculating the PDF with the fit variable
# that we give it.
MnOFit = FitRecipe()

# give the PDFContribution to the FitRecipe
MnOFit.addContribution(MnOPDF)

# Configure the fit variables and give them to the recipe.  We can use the
# srfit function constrainAsSpaceGroup to constrain the lattice and ADP
# parameters according to the H-3m space group.
from diffpy.srfit.structure import constrainAsSpaceGroup
spaceGroupParams = constrainAsSpaceGroup(MnOPDF.MnO.phase, spaceGroup)
print("Space group parameters are:", end=' ')
print(', '.join([p.name for p in spaceGroupParams]))
print()

# We can now cycle through the parameters and activate them in the recipe as
# variables
for par in spaceGroupParams.latpars:
    MnOFit.addVar(par)
# Set initial value for the ADP parameters, because CIF had no ADP data.
for par in spaceGroupParams.adppars:
    MnOFit.addVar(par, value=0.003,fixed=True)

# As usual, we add variables for the overall scale of the PDF and a delta2
# parameter for correlated motion of neighboring atoms.
MnOFit.addVar(MnOPDF.scale, 1)
MnOFit.addVar(MnOPDF.MnO.delta2, 1.5)

# We fix Qdamp based on prior information about our beamline.
MnOFit.addVar(MnOPDF.qdamp, 0.03, fixed=True)

# Turn off printout of iteration number.
MnOFit.clearFitHooks()

# We can now execute the fit using scipy's least square optimizer.
print("Refine PDF using scipy's least-squares optimizer:")
print("  variables:", MnOFit.names)
print("  initial values:", MnOFit.values)
leastsq(MnOFit.residual, MnOFit.values)
print("  final values:", MnOFit.values)
print()

# Obtain and display the fit results.
MnOResults = FitResults(MnOFit)
print("FIT RESULTS\n")
print(MnOResults)

# Get the experimental data from the recipe
r = MnOFit.MnO.profile.x
gobs = MnOFit.MnO.profile.y

# Get the calculated PDF and compute the difference between the calculated and
# measured PDF
gcalc = MnOFit.MnO.evaluate()
baseline = 1.1 * gobs.min()
gdiff = gobs - gcalc
baseline2 = 1.2 * (gdiff+baseline).min()

### NOW DO THE MPDF REFINEMENT USING THE RESIDUAL FROM THE ATOMIC PDF
mc.rmin = r.min()
mc.rmax = r.max()
def residual(p, yexp, mcalc):
    mcalc.paraScale, mcalc.ordScale = p
    return yexp - mcalc.calc(both=True)[2]

p0 = [5.0, 3.0] # initial parameter values (parScale, ordScale)
pOpt = leastsq(residual, p0, args=(gdiff,mc))
print(pOpt)

fit=mc.calc(both=True)[2]

# Plot!
ax=plt.figure().add_subplot(111)
ax.plot(r, gobs, 'bo', label="Total PDF",markerfacecolor='b', markeredgecolor='b')
ax.plot(r, gdiff + baseline,mfc='Indigo',mec='Indigo',marker='o',linestyle='none',label='mPDF')
ax.plot(r, gcalc, 'r-', lw=2.5, label="Fit")
ax.plot(r, fit+baseline,'r-',lw=2.5)
ax.plot(r, gdiff - fit + baseline2, 'g-', label='Residual')
ax.plot(r, np.zeros_like(r) + baseline2, 'k:')
ax.set_xlabel('r ($\AA$)', fontsize=16)
ax.set_ylabel('G, d ($\AA^{-2}$)', fontsize=16)
ax.set_xlim(xmin=0, xmax=20)
#ax.set_yticks([])
#ax.set_yticklabels([])
plt.legend()

plt.tight_layout()
plt.show()
