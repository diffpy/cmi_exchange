# CMI Plugins

Here you will find community developed functions and IPython plugins related to the DiffPy-CMI
complex modeling framework.
CMI Plugins require that the parent cmi_exchange directory is in
the Python module path, so that any given plugin can be imported
in Python using

```python
import cmi_plugins.SomeName
```

See the [Python Path Instructions](./PYPATH.md) for details on
adding the cmi_exchange directory to Python path.


## Contents

### [cmi_plugins.ipy_gaussianfit](./ipy_gaussianfit.py)

IPython extension to fit a Gaussian peak to a set of data using the SrFit
framework.  Provides GaussianFit class and fitGaussian function.

To activate in an IPython session use `%load_ext cmi_plugins.ipy_gaussianfit`.
For use in Python scripts import the code as `cmi_plugins.ipy_gaussianfit`.

To try out the class execute the following commands:

```python
from cmi_plugins.ipy_gaussianfit import GaussianFit
import numpy as np

x = np.arange(-10, 10, 0.1)
x0, sig = -2, 1.5
noise = 0.2 * np.ones_like(x)
y = np.exp(-0.5*(x-x0)**2/sig**2) + noise * np.random.randn(*x.shape)
gfit = GaussianFit(x, y, noise)
gfit.refine()
gfit.plot()
```

x, y, dy are the data to be fitted with Gaussian peak (dy may be omitted)
A, sig, and x0 are initial values.  If omitted the program will estimate
their starting values.


## More information on IPython

[IPython extensions](http://ipython.org/ipython-doc/stable/config/extensions/index.html)
are importable IPython modules that can modify the behavior of the shell to
add functionality.  They are activated from the IPython command line by running

    %load_ext python_name_of_extenstion

To have certain extensions available at startup first make sure that
the IPython user profile exists and determine its location by running
in a system shell

```sh
ipython profile create     # create default user profile
ipython locate profile     # print location of user profile
```

Edit the `ipython_config.py` file in the profile directory
and modify the `c.InteractiveShellApp.extensions` variable
as necessary.  See
[IPython documentation](http://ipython.org/ipython-doc/stable/config/)
for an exhaustive details.
