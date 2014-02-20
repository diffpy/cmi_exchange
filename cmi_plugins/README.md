# CMI Plugins

Here you will find community developed functions and IPythons plugins related to the DiffPy-CMI
complex modeling framework.

Contents
--------

* [ipy_gaussianfit.py](./ipy_gaussianfit.py) - IPython extension to fit a Gaussian peak to a set of data using the SrFit framework.

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


More information on IPython 
---------------------------

[IPython
extensions](http://ipython.org/ipython-doc/rel-0.12.1/config/extensions/index.html)
are importable IPython modules that can modifpy the behavior of the shell to
add functionality.  They are installed from the IPython command line by running

    %install_ext name_of_extension.py

and activated by running

    %load_ext name_of_extenstion 

To have certain extensions available at startup modify the
c.InteractiveShellApp.extensions variable in ipython_config.py.
