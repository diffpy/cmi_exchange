# Python Path Instructions

[CMI Plugins](./README.md) require that the parent cmi_exchange directory
is present in the Python search path, also called PYTHONPATH.  There are
several ways how to accomplish this as discussed below.


## Use pth file

This is the preferred way of extending PYTHONPATH.  On startup
Python checks several locations, named site directories, for `.pth` files,
and then adds each line from every .pth file (unless commented out)
to its internal PYTHONPATH.  The site directories come in two flavors -
*user site*, which is processed only for a specific user, and
*distribution site*, which applies for everyone using the same Python
installation.  In addition, some Python installations are configured to
ignore the user site directory, which is controlled by the
`ENABLE_USER_SITE` flag in the site module.  This flag can be
checked by running in system shell

```sh
python -m pydoc site
```

and using "G" to scroll to a very bottom of the document.  The next
shell command takes all these eventualities into account and displays
potential site directories that should process the .pth files:

```sh
python -c "import site; \
    print (site.getusersitepackages() if site.ENABLE_USER_SITE \
        else '\n'.join(site.getsitepackages()))"
```

Note that some of those directories may not exist, especially the user
site directory is often left for the user to create.  If necessary, the
user site folder can be created with

```sh
mkdir -p /wherever/is/user/site
```

Finally, once the site directory is determined and known to exist,
navigate to the root *cmi_exchange* directory in the terminal and run the
following command:

```sh
pwd > cmi_exchange.pth
```

This will create the cmi_exchange.pth file.  Move this file to the
site directory, e.g., `mv cmi_exchange.pth /wherever/is/site/dir/`,
and all should be now set.  To check if the new path works, run

```sh
python -m pydoc cmi_plugins
```

which should display a brief description for the content of cmi_plugins.


## Use symbolic link


Another option is to create a symbolic link to the *cmi_plugins* directory
in one of the directories that is already in Python path.  To Python this will
appear to as if cmi_plugins were a subdirectory in one of its paths.  To print
out the list of the active Python paths, use

```sh
python -c "import sys; print '\n'.join(sys.path)"
```

Select one of those directories and then navigate to the root
*cmi_exchange* directory and run the following command

```sh
ln -si $PWD/cmi_plugins /the/selected/directory/
```

As above, the installation of cmi_plugins can be tested using

```sh
python -m pydoc cmi_plugins
```


## Use the PYTHONPATH environment variable

Python module path can be also extended by setting the *PYTHONPATH*
environment variable so that it contains a full path to the root
*cmi_exchange* directory.  Determine your shell startup file (usually
one of `.profile`, `.bash_profile`, `.zshenv`) and add there the
following line:

```sh
export PYTHONPATH="/wherever/is/cmi_exchange:${PYTHONPATH}"
```

You may need to restart the shell or source the setup file manually
for this to take effect.  The active environment can be checked
by running

```sh
env | grep PYTHONPATH
```

To verify if Python can find cmi_plugins, use

```sh
python -m pydoc cmi_plugins
```
