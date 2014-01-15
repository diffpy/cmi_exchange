#!/usr/bin/env python
# -*- coding: utf-8 -*-

from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import PDFCalculator
from matplotlib.pyplot import plot, show

cds = loadStructure('CdS_wurtzite.cif')
pc1 = PDFCalculator()
pc1.rmax = 20
pc1.scatteringfactortable.setCustomAs('S2-', 'S', 18)
pc1.scatteringfactortable.lookup('S2-')
r1, g1 = pc1(cds)
plot(r1, g1)

pc2 = pc1.copy()
cds2 = loadStructure('CdS_wurtzite.cif')
cds2.anisotropy = False
r2, g2 = pc2(cds2)
plot(r2, g2)
plot(r1, g1-g2)
show()
