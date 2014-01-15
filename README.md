srfit-demos
===========

example scripts for the diffpy.srfit data fitting framework

This project is a collection of examples for learning the diffpy.srfit and
diffpy.srreal Python libraries. diffpy.srfit is a data optimization framework
designed for fitting crystal structure models to experimental data.
diffpy.srreal is a set of calculators for pair distribution function, bond
valence sums from a known crystal structure model.


IPython extension
-----------------

This is an example of defining a Gaussian peak fit using SrFit and
its sharing as IPython extension.

Usage in IPython shell:

Install this extension with

    %install_ext https://raw.github.com/diffpy/srfit-demos/master/ipyplugin/gaussianfit.py

Activate this extension using

    %load_ext gaussianfit

or adjust the c.InteractiveShellApp.extensions variable in ipython_config.py
to load it at startup every time.


To try out the class execute the following commands:

    import numpy as np
    x = np.arange(-10, 10, 0.1)
    x0, sig = -2, 1.5
    noise = 0.2 * np.ones_like(x)
    y = np.exp(-0.5*(x-x0)**2/sig**2) + noise * np.random.randn(*x.shape)
    gfit = GaussianFit(x, y, noise)
    gfit.refine()
    gfit.plot()

x, y, dy are the data to be fitted with Gaussian peak (dy may be omitted)
A, sig, and x0 are initial values.  If omitted the program will estimate
their starting values.
