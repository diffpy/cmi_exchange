import numpy as np
import matplotlib.pyplot as plt

# DiffPy-CMI modules for building a fitting recipe
from diffpy.Structure import loadStructure

from diffpy.magpdf import *

# Files containing our experimental data and structure file
structureFile = "MnO_cubic.cif"

# Create the structure from our cif file
mnostructure = loadStructure(structureFile)
# modify the structure to simulate a 1-D material
mnostructure.lattice.a=3.0
mnostructure.lattice.b=150.0
mnostructure.lattice.c=150.0

# Create a magnetic species object
helix=magSpecies(mnostructure)

# Set up the basis vectors for a helical spin configuration
Sk=0.5*(np.array([0,0,1])+0.5j*np.array([0,1,0]))
helix.basisvecs=np.array([Sk,Sk.conj()])

# Set up the propagation vector
helix.kvecs=np.array([[np.sqrt(2)/10,0,0],[-1.0*np.sqrt(2)/10,0,0]])

# Populate with atoms and spins
helix.rmaxAtoms=70.0
helix.makeAtoms()
helix.makeSpins()
helix.label='helix'

# Create the magnetic structure object
mstruc=magStructure()
mstruc.loadSpecies(helix)
mstruc.makeAll()

# Visualize the spins
x,y,z=mstruc.atoms.transpose()
mask=np.logical_and(z==0,np.logical_and(y==0,np.abs(x)<30))
visatoms=mstruc.atoms[mask]
visspins=spinsFromAtoms(mstruc,visatoms,fractional=False)
mstruc.visualize(visatoms,visspins)

# Create the mPDF calculator
mc=mPDFcalculator(mstruc)
mc.rmax=70.0

mc.plot()
