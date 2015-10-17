# CMI Scripts

This is a set of community developed stand-alone Python scripts that use the
DiffPy-CMI packages for a range of data fitting and visualization tasks. These
can be used as tutorial examples or can be adapted to solve a particular
problem you are interested in.

Contents
--------

* [calcbvsnacl](./calcbvsnacl) - Calculate bond valence sums for NaCl
  using standard and custom valence parameters.

* [calcpdfc60](./calcpdfc60) - Calculate and plot a PDF for C60 from a stru
  file. Uses the DebyePDFCalculator from DiffPy-CMI.

* [calcpdfcds](./calcpdfcds) - Calculate and plot a PDF for CdS wurtzite from
  a cif file. Uses the PDFCalculator module from DiffPy-CMI.

* [fitCdSeNP](./fitCdSeNP) - Fit the PDF of CdSe nanoparticles using a
  non-periodic structure model.

* [fitNaClBVS](./fitNaClBVS) - Fit X-ray PDF data from NaCl with a restraint
  for bond valence sums in the structure.

* [fitNiPDF](./fitNiPDF) - Fit a neutron PDF data from nickel using a periodic structure
  model.

* [linearfit](./linearfit) - Perform a simple linear fit to a set of noisy
  data. This script can be run in IPython "demo" mode or as an IPython
  notebook.

* [pdfrectprofile](./pdfrectprofile) - Demonstrate definition of custom
  profile for PDF calculation.

More information on IPython
---------------------------

Some of the above examples are written as IPython notebooks (extension
.ipynb).  An IPython notebook creates an interactive computational environment
similar to Mathematica.  To start notebook mode in IPython, run the command

    ipython notebook

You can then load the .ipynb file directly into your workspace. Alternatively,
you can run

    ipython notebook name_of_notebook.ipynb

to load the notebook file directly. You can then interactivly run the script
step by step, changing individual parts and updating the result by typing
"Ctrl+Enter".


* For more information visit the [IPython
  notebook](http://ipython.org/notebook.html) documentation page
