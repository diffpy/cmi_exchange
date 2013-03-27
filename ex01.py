# coding: utf-8
cds=loadStructure('CdS_wurtzite.cif')
pc1=PDFCalculator()
pc1.scatteringfactortable.setCustomAs('S2-', 'S', 18)
pc1.scatteringfactortable.lookup('S2-')
r1,g1=pc1(cds)
plot(r1,g1)
