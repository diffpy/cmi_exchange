# cmi_exchange

This project is a community developed collection of sample scripts, functions
and IPython plugins related to the DiffPy-CMI complex modeling framework.

cmi_plugins is for IPython plugins ... FIXME

collection of examples for learning the diffpy.srfit data fitting framework. Currently it includes examples of:

* diffpy.srfit
* diffpy.srreal
* ipython extension 


diffpy.srfit
------------

diffpy.srfit is a data optimization framework designed for fitting crystal structure models to experimental data. 

Here is an example for a simple linear fit to a noisy data. This script can be run in IPython "demo" mode.  To use the demo mode, start IPython and execute the following commands:

    In [1]: %run LinerFit.py demo
    In [2]: demo()
    ...
    In [3]: demo()
    ...


diffpy.srreal
-------------

diffpy.srreal is a set of calculators for pair distribution function, bond valence sums from a known crystal structure model.

Here are examples for calculating the pair distribution function of C60 (discrete particles) and CdS (bulk materials). 


IPython notebook
----------------

Part of examples have IPython notebook version. To start the IPython notebook mode, run the command

    ipython notebook
    
Then you can load the .ipynb file into the workspace or alternatively run 

    ipython notebook name_of_notebook.ipynb

to load the notebook file directly. Then you can interactivly run the scirpt step by step. In each cell of codes, you can try to change the scripts and see the results by running the code cell using "Ctrl+Enter".

For more details of the usage of IPython notebook, please refer to http://ipython.org/ipython-doc/stable/interactive/notebook.html. 


IPython extension
-----------------

diffpy.srfit (and other diffpy projects) can be easily extended. Here is an example of defining a Gaussian peak fit using SrFit and its sharing as IPython extension.

Usage in IPython shell (IPython verison > 1.0):

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
