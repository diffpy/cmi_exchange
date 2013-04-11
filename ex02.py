# coding: utf-8
c60=loadStructure('c60.stru')
dpc=DebyePDFCalculator()
dpc.qmax=20
dpc.rmax=20
r3,g3=dpc(c60, qmin=0)
r4,g4=dpc(c60, qmin=1)