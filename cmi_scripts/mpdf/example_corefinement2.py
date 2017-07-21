#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This example will show how to simultaneously refine the atomic and magnetic PDF
of MnO using SrFit. First, we refine each component separately, then we refine
them together. Doing it in steps like this can be useful to help the combined
fit converge more quickly.
'''

# Import necessary functions
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

from diffpy.mpdf import *
from diffpy.Structure.Parsers import getParser
from diffpy.srfit.pdf import PDFGenerator, PDFParser
from diffpy.srfit.fitbase import FitRecipe, FitResults
from diffpy.srfit.fitbase import Profile, FitContribution

# Files containing our experimental data and structure file
dataFile = "npdf_07334.gr"
structureFile = "MnO_R-3m.cif"

# load structure and space group from the CIF file
pcif = getParser('cif')
mno = pcif.parseFile(structureFile)

# prepare profile object with experimental data
profile = Profile()
parser = PDFParser()
parser.parseFile(dataFile)
profile.loadParsedData(parser)

# define range for pdf calculation
rmin = 0.01
rmax = 20
rstep = 0.01

# setup calculation range for the PDF simulation
profile.setCalculationRange(xmin=rmin, xmax=rmax, dx=rstep)

# prepare nucpdf function that simulates the nuclear PDF
nucpdf = PDFGenerator("nucpdf")
nucpdf.setStructure(mno)
nucpdf.setProfile(profile)


### DO AN INITIAL FIT TO THE STRUCTURAL PDF
totpdf=FitContribution('totpdf')
totpdf.addProfileGenerator(nucpdf)
totpdf.setProfile(profile)
totpdf.setEquation("nucscale*nucpdf")

# The FitRecipe does the work of calculating the PDF with the fit variables
# that we give it.
mnofit = FitRecipe()

# give the FitContribution to the FitRecipe
mnofit.addContribution(totpdf)

# Configure the fit variables and give them to the recipe.  We can use the
# srfit function constrainAsSpaceGroup to constrain the lattice and ADP
# parameters according to the CIF-loaded space group.
from diffpy.srfit.structure import constrainAsSpaceGroup
sgpars = constrainAsSpaceGroup(nucpdf.phase, pcif.spacegroup.short_name)
print("Space group parameters are:", end=' ')
print(', '.join([p.name for p in sgpars]))
print()

# We can now cycle through the parameters and activate them in the recipe as
# variables
for par in sgpars.latpars:
    mnofit.addVar(par)
# Set initial value for the ADP parameters, because CIF had no ADP data.
for par in sgpars.adppars:
    mnofit.addVar(par,value=0.003)

# As usual, we add variables for the overall scale of the PDF and a delta2
# parameter for correlated motion of neighboring atoms.
mnofit.addVar(totpdf.nucscale, 1)
mnofit.addVar(nucpdf.delta2, 1.5)

# We fix Qdamp based on prior information about our beamline.
mnofit.addVar(nucpdf.qdamp, 0.03)

# Turn off printout of iteration number.
mnofit.clearFitHooks()

# Initial structural fit
print("Refine PDF using scipy's least-squares optimizer:")
print("  variables:", mnofit.names)
print("  initial values:", mnofit.values)
leastsq(mnofit.residual, mnofit.values)
print("  final values:", mnofit.values)
print()
# Obtain and display the fit results.
mnoresults = FitResults(mnofit)
print("FIT RESULTS\n")
print(mnoresults)

# Get the experimental data from the recipe
r = mnofit.totpdf.profile.x
gobs = mnofit.totpdf.profile.y

# Get the calculated PDF and compute the difference between the calculated and
# measured PDF
gcalc = mnofit.totpdf.evaluate()
baseline = 1.1 * gobs.min()
gdiff = gobs - gcalc

# Plot the structural refinement
ax=plt.figure().add_subplot(111)
ax.plot(r, gobs, 'bo', label="G(r) data",markerfacecolor='none', markeredgecolor='b')
ax.plot(r, gcalc, 'r-', lw=1.5, label="G(r) fit")
ax.plot(r, gdiff + baseline,'g-')
ax.plot(r, np.zeros_like(r) + baseline, 'k:')

ax.set_xlabel(r"r ($\AA$)")
ax.set_ylabel(r"G ($\AA^{-2}$)")
plt.legend()

plt.show()

### NOW DO THE INITIAL MAGNETIC REFINEMENT

# Create the Mn2+ magnetic species
mn2p = MagSpecies(struc=mno, label='Mn2+', magIdxs=[0,1,2],
                  basisvecs=2.5*np.array([1,0,0]), kvecs=np.array([0,0,1.5]),
                  ffparamkey='Mn2')

# Create and prep the magnetic structure
mstr = MagStructure()
mstr.loadSpecies(mn2p)
mstr.makeAll()

# Set up the mPDF calculator.

mc=MPDFcalculator(magstruc=mstr,rmin=rmin,rmax=rmax,
                  rstep=rstep, gaussPeakWidth=0.2)

# Do the refinement
def magresidual(p, yexp, mcalc):
    mcalc.paraScale,mcalc.ordScale = p
    return yexp-mcalc.calc(both=True)[2]

p0=[5.0,3.0] # initial parameter values (paraScale, ordScale)
pOpt=leastsq(magresidual, p0, args=(gdiff, mc))
print(pOpt)

magfit = mc.calc(both=True)[2]
magdiff = gdiff - magfit
magbaseline = 1.1*gdiff.min()

# Plot!
ax = plt.figure().add_subplot(111)
ax.plot(r, gdiff, 'bo', label="G(r) data",markerfacecolor='none', markeredgecolor='b')
ax.plot(r, magfit, 'r-', lw=1.5, label="G(r) fit")
ax.plot(r, magdiff + magbaseline,'g-')
ax.plot(r, np.zeros_like(r) + magbaseline, 'k:')
ax.set_xlabel(r"r ($\AA$)")
ax.set_ylabel(r"G ($\AA^{-2}$)")
plt.legend()

plt.show()


### NOW DO THE CO-REFINEMENT OF STRUCTURAL AND MAGNETIC PDF
def mpdf(parascale, ordscale):
    mc.paraScale = parascale
    mc.ordScale = ordscale
    mc.magstruc.makeAtoms()
    mc.magstruc.makeSpins()
    rv = mc.calc(both=True)[2]
    return rv

# Add the mPDF to the totpdf FitContribution
totpdf.registerFunction(mpdf)
totpdf.setEquation("nucscale * nucpdf + mpdf(parascale, ordscale)")

# Make magnetic PDF depend on any changes to the atomic structure.
# Cover your eyes, but a structure change will now trigger the same
# reevaluations as if ordscale were modified.
nucpdf.phase.addObserver(totpdf.ordscale.notify)

# add the mPDF variables
mnofit.addVar(totpdf.parascale,value=mc.paraScale)
mnofit.addVar(totpdf.ordscale,value=mc.ordScale)

# do the co-refinement
print("Refine PDF using scipy's least-squares optimizer:")
print("  variables:", mnofit.names)
print("  initial values:", mnofit.values)
leastsq(mnofit.residual, mnofit.values)
print("  final values:", mnofit.values)
print()
mnoresults=FitResults(mnofit)
print("FIT RESULTS\n")
print(mnoresults)

# Get the calculated PDF and compute the difference between the calculated and
# measured PDF
gcalc = mnofit.totpdf.evaluate()
gnuc = mnofit.totpdf.evaluateEquation('nucscale * nucpdf')
gmag = mnofit.totpdf.evaluateEquation('mpdf')

baseline = 1.1 * gobs.min()
gdiff = gobs - gcalc
baseline2 = 1.1 * (gdiff+baseline).min()
magfit=mc.calc(both=True)[2]

# Plot the observed and refined total PDF.
ax=plt.figure().add_subplot(111)
ax.plot(r, gobs, 'bo', label="G(r) data",markerfacecolor='none', markeredgecolor='b')
ax.plot(r, gcalc, 'r-', lw=2.5, label="G(r) fit")
ax.plot(r, gdiff + baseline,'g-')
ax.plot(r, np.zeros_like(r) + baseline, 'k:')
ax.set_xlabel(r"r ($\AA$)")
ax.set_ylabel(r"G ($\AA^{-2}$)")
ax.set_xlim(xmax=mc.rmax)
plt.legend()

plt.show()
