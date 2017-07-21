#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import matplotlib.pyplot as plt
from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import PDFCalculator
from rectangleprofile import RectangleProfile

ni = loadStructure('ni.cif')
# The CIF file had no displacement data so we supply them here:
ni.Uisoequiv = 0.005

# Calculate PDF with default profile function
pc1 = PDFCalculator()
r1, g1 = pc1(ni)
print("standard peakprofile:\n    " + repr(pc1.peakprofile))

# Create new calculator that uses the custom profile function
pc2 = PDFCalculator()
pc2.peakprofile = RectangleProfile()
# Note:  pc2.peakprofile = 'rectangleprofile'
# would do the same, because RectangleProfile class was registered
# under its 'rectangleprofile' identifier.
print("custom peakprofile:\n    " + repr(pc1.peakprofile))
r2, g2 = pc2(ni)

# compare both simulated curves
plt.plot(r1, g1, r2, g2)
plt.draw()
plt.show()
