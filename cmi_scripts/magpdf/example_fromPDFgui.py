import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from diffpy.Structure import loadStructure

from diffpy.magpdf import *

# Create the structure from our cif file, update the lattice params
structureFile = "MnO_R-3m.cif"
mnostructure = loadStructure(structureFile)
lat=mnostructure.lattice
lat.a,lat.b,lat.c=3.1505626,3.1505626,7.5936979

# Create the Mn2+ magnetic species
mn2p=magSpecies(struc=mnostructure,label='Mn2+',magIdxs=[0,1,2],basisvecs=2.5*np.array([1,0,0]),kvecs=np.array([0,0,1.5]),ffparamkey='Mn2')

# Create and prep the magnetic structure
magstruc=magStructure()
magstruc.loadSpecies(mn2p)
magstruc.makeAtoms()
magstruc.makeSpins()
magstruc.makeFF()

# 
# Set up the mPDF calculator
mc=mPDFcalculator(magstruc=magstruc,rmax=20.0,gaussPeakWidth=0.2)


# Load the data
PDFfitFile='MnOfit_PDFgui.fgr'
rexp,Drexp=getDiffData([PDFfitFile])
mc.rmin=rexp.min()
mc.rmax=rexp.max()

# Do the refinement
def residual(p,yexp,mcalc):
    mcalc.paraScale,mcalc.ordScale=p
    return yexp-mcalc.calc(both=True)[2]

p0=[5.0,3.0]
pOpt=leastsq(residual,p0,args=(Drexp,mc))
print pOpt

fit=mc.calc(both=True)[2]

# Plot the results
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(rexp,Drexp,marker='o',mfc='none',mec='b',linestyle='none')
ax.plot(rexp,fit,'r-',lw=2)
ax.set_xlim(xmin=mc.rmin,xmax=mc.rmax)
ax.set_xlabel('r ($\AA$)')
ax.set_ylabel('d(r) ($\AA^{-2}$)')

plt.show()


