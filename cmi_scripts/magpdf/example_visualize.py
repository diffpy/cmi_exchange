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

# Create the magnetic species
mn2p=magSpecies(label='Mn',struc=mnostructure)
mn2p.magIdxs=[0,1,2,3]
mn2p.basisvecs=np.array([[1,-1,0]])
mn2p.kvecs=np.array([[0.5,0.5,0.5]])
mn2p.ffparamkey='Mn2'

# Create a magnetic structure object
magstruc=magStructure(mnostructure)
magstruc.loadSpecies(mn2p)

# Generate the atomic positions, spins, and form factor
magstruc.makeAtoms()
magstruc.makeSpins()
magstruc.makeFF()

visatoms=mnostructure.lattice.cartesian(np.array([[0,0,0],[0.5,0.5,0],[0.5,0,0.5],[0,0.5,0.5]]))
visspins=np.array(spinsFromAtoms(magstruc,visatoms,fractional=False))
magstruc.visualize(visatoms,visspins,showcrystalaxes=True)
#fig=visualizeSpins(visatoms,visspins)
