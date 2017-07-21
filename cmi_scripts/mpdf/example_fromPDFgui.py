#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This example will show how to perform mPDF refinements after having done the atomic
PDF refinement in PDFgui. We use data from MnO at 15 K.
'''

# Import necessary functions
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

from diffpy.mpdf import *
from diffpy.Structure import loadStructure

# Create the structure from our cif file, update the lattice params
structureFile = "MnO_R-3m.cif"
mnostructure = loadStructure(structureFile)
lat = mnostructure.lattice
lat.a,lat.b,lat.c = 3.1505626,3.1505626,7.5936979 ## refined values from PDFgui

# Create the Mn2+ magnetic species
mn2p = MagSpecies(struc=mnostructure, label='Mn2+', magIdxs=[0,1,2],
                 basisvecs=2.5*np.array([1,0,0]), kvecs=np.array([0,0,1.5]),
                 ffparamkey='Mn2')

# Create and prep the magnetic structure
mstr = MagStructure()
mstr.loadSpecies(mn2p)
mstr.makeAtoms()
mstr.makeSpins()
mstr.makeFF()

# Set up the mPDF calculator
mc = MPDFcalculator(magstruc=mstr, gaussPeakWidth=0.2)

# Load the data
PDFfitFile = 'MnOfit_PDFgui.fgr'
rexp,Drexp = getDiffData([PDFfitFile]) # this reads in the fit file
mc.rmin = rexp.min()
mc.rmax = rexp.max()

# Do the refinement
def residual(p, yexp, mcalc):
    mcalc.paraScale, mcalc.ordScale = p
    return yexp-mcalc.calc(both=True)[2]

p0 = [5.0,3.0] # initial parameter values (paraScale, ordScale)
pOpt = leastsq(residual, p0, args=(Drexp,mc))
print(pOpt)

fit=mc.calc(both=True)[2]

# Plot the results
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(rexp, Drexp, marker='o', mfc='none', mec='b', linestyle='none')
ax.plot(rexp, fit, 'r-', lw=2)
ax.set_xlim(xmin=mc.rmin, xmax=mc.rmax)
ax.set_xlabel('r ($\AA$)')
ax.set_ylabel('d(r) ($\AA^{-2}$)')

plt.show()
