#!/usr/bin/env python
# -*- coding: utf-8 -*-

from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import DebyePDFCalculator
from matplotlib.pyplot import plot, show

c60 = loadStructure('c60.stru')
dpc = DebyePDFCalculator()
dpc.qmax = 20
dpc.rmax = 20
r3, g3 = dpc(c60, qmin=0)
r4, g4 = dpc(c60, qmin=1)

plot(r3, g3, r4, g4)
show()
