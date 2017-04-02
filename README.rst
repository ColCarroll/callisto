|Build Status| |Coverage Status|

========
Callisto
========


*The fourth Galilean moon of Jupyter.*

A command line utility to create kernels in Jupyter from virtual environments.

Installation
============
Callisto may be installed `from pypi <https://pypi.python.org/pypi/callisto>`_:
::

    pip install callisto



Basic Usage.
============
Typical use is to just activate it inside a virtual environment:
::

    $ source venv/bin/activate
    (venv) $  callisto
    Successfully installed a new jupyter kernel "venv":
    {
      "env": {},
      "language": "python",
      "display_name": "venv",
      "argv": [
        "/Users/colin/projects/pete/venv/bin/python",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
      ]
    }
    See /Users/colin/Library/Jupyter/kernels/venv/kernel.json to edit.

Jupyter servers will now have an option for a kernel called `venv`.

Naming the kernel.
==================
You may also give kernels a more descriptive name:
::

    (venv) $  callisto -n pete
    Successfully installed a new jupyter kernel "pete":
    {
      "env": {},
      "display_name": "pete",
      "argv": [
        "/Users/colin/projects/pete/venv/bin/python",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
      ],
      "language": "python"
    }
    See /Users/colin/Library/Jupyter/kernels/pete/kernel.json to edit.

Jupyter servers will now have an option for a kernel called `venv`, and `pete`.


Deleting kernels.
=================
Sometimes you may want to tidy kernels up a bit.
::

    (venv) $  callisto -d
    Deleted jupyter kernel "venv" from /Users/colin/Library/Jupyter/kernels/venv/kernel.json:
    {
      "argv": [
        "/Users/colin/projects/pete/venv/bin/python",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
      ],
      "env": {},
      "language": "python",
      "display_name": "venv"
    }

Jupyter servers will no longer have a kernel named `venv`.



Lacking courage.
================
Callisto doesn't try to be too clever.
::

    (venv) $  deactivate

    $  callisto
    Usage: callisto [OPTIONS]

    Error: The environment variable VIRTUAL_ENV is not set (usually this is set
    automatically activating a virtualenv).  Please make sure you are in a
    virtual environment!

Viewing existing kernels.
=========================
If you forgot the informative message about the kernel information, you can see it later.
::

    $  source venv/bin/activate

    (venv) $  callisto --list
    No kernel found at /Users/colin/Library/Jupyter/kernels/venv/kernel.json

    (venv) $  callisto -l --name pete
    Found kernel "pete" at /Users/colin/Library/Jupyter/kernels/pete/kernel.json:
    {
      "display_name": "pete",
      "language": "python",
      "argv": [
        "/Users/colin/projects/pete/venv/bin/python",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
      ],
      "env": {}
    }



Adjusting the `PYTHONPATH`.
===========================
With isolated kernels, you may wish to run all your notebooks from a single directory,
but using code from the project directories.
::

    (venv) $  callisto -n pete --path=/Users/colin/projects/pete/
    Successfully installed a new jupyter kernel "pete":

    {
      "argv": [
        "/Users/colin/projects/pete/venv/bin/python",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
      ],
      "language": "python",
      "env": {
        "PYTHONPATH": "/Users/colin/projects/pete:PYTHONPATH"
      },
      "display_name": "pete"
    }
    See /Users/colin/Library/Jupyter/kernels/pete/kernel.json to edit.

Now the `pete` kernel will be able to import from the folder `/Users/colin/projects/pete`.

.. |Build Status| image:: https://travis-ci.org/ColCarroll/callisto.svg?branch=master
   :target: https://travis-ci.org/ColCarroll/callisto
.. |Coverage Status| image:: https://coveralls.io/repos/github/ColCarroll/callisto/badge.svg?branch=master
   :target: https://coveralls.io/github/ColCarroll/callisto?branch=master
