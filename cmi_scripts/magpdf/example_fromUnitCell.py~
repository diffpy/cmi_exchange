import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from diffpy.Structure import loadStructure

from diffpy.magpdf import *

# Create the magnetic species
msp=magSpecies(useDiffpyStruc=False)
msp.latVecs=np.array([[4,0,0],
                      [0,4,0],
                      [0,0,4]])

msp.atomBasis=np.array([[0,0,0],
                        [0.5,0.5,0.5]])

msp.spinBasis=np.array([[0,0,1],
                        [0,0,-1]])

# Create the magnetic structure
mstr=magStructure()
mstr.loadSpecies(msp)
mstr.makeAtoms()
mstr.makeSpins()

# Set up the mPDF calculator
mc=mPDFcalculator(magstruc=mstr)

mc.plot()
