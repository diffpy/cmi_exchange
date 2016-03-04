import numpy as np
import matplotlib.pyplot as plt

# DiffPy-CMI modules for building a fitting recipe
from diffpy.Structure import loadStructure

from diffpy.magpdf import *

# Files containing our experimental data and structure file
structureFile = "MnO_cubic.cif"

# Create the structure from our cif file
#
mnostructure = loadStructure(structureFile)

# Create a magnetic structure object
magstruc=magStructure(mnostructure)

# Create a magnetic species object
magstruc.makeSpecies('Mn')
magstruc.species['Mn'].magIdxs=[0,1,2,3]
magstruc.species['Mn'].basisvecs=np.array([[1,-1,0]])
magstruc.species['Mn'].kvecs=np.array([[0.5,0.5,0.5]])
magstruc.species['Mn'].ffparamkey='Mn2'

# Generate the atomic positions, spins, and form factor
magstruc.makeAtoms()
magstruc.makeSpins()
magstruc.makeFF()

# Create an mPDFcalculator object and feed it a magnetic structure
mc=mPDFcalculator(magstruc)

r,fr,Dr=mc.calc(both=True)
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(r,fr,'r-',r,Dr,'b-')
ax.set_xlabel('r ($\AA$)')
ax.set_ylabel('f ($\AA^{-2}$)')

plt.show()

