#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Calculation of bond valence sums using diffpy.srreal module included in
DiffPy-CMI.
'''

from __future__ import print_function
from diffpy.Structure import loadStructure
from diffpy.srreal.bvscalculator import BVSCalculator

# load crystal structure data from a CIF file
nacl = loadStructure('NaCl.cif')

# create bond valence sum calculator object
bvsc = BVSCalculator()

# calculate BVS and print the expected and actual valences
vsim = bvsc(nacl)
print('Calculate bond valence sums for NaCl "bvsc(nacl)"')
print('expected "bvsc.valences":\n ', bvsc.valences)
print('calculated "bvsc.value":\n ' , vsim)
print('difference "bvsc.bvdiff":\n ', bvsc.bvdiff)
print('root mean square difference "bvsc.bvrmsdiff":', bvsc.bvrmsdiff)
print()

# create new BVS calculator with a custom bond valence parameters
bvsc2 = BVSCalculator()

# Use alternate value for the Na+ Cl- bond valence parameters from
# http://www.iucr.org/__data/assets/file/0018/59004/bvparm2011.cif
# These parameters have 6A cutoff.
bvsc2.bvparamtable.setCustom('Na', +1, 'Cl', -1, Ro=1.6833, B=0.608)
bvsc2.rmax = 6
print("BVS in NaCl with alternate parameters:\n ", bvsc2(nacl))
print()

# Lookup table of bond valence parameters can be used as separate object.
from diffpy.srreal.bvparameterstable import BVParametersTable

table = BVParametersTable()
bp = table.lookup('Na+', 'Cl-')
bp2 = table.lookup('Na', +1, 'Br', -1)
print("Standard lookup of bond valence parameters:")
print(" ", bp)
print(" ", bp2)
print()

print("Handling of unknown or invalid ion pairs:")
print("  table.lookup('A+', 'X-'):", table.lookup('A+', 'X-'))
print("  table.lookup('A+', 'X-') == table.none():",
      table.lookup('A+', 'X-') == table.none())
