tidy_interface
==============

|docs|

**tidy_interface** is a signal interface management tool for managing interface signals across different versions. Detailed documentation can be found [here](https://tidy-interface.readthedocs.io/en/).

Dependencies
------------

This tool uses Python, Django, SQLite3, pyyaml for database management. If you access this tool through ``pip install tidy-interface``, then you do not need to worry about manually installing dependencies.

For developers, you may want to build this tool from source. In this case, you'll need to mannually install dependencies. 

To manually install dependencies, it is recommended to first create a virtual environment. To create a virtual environment, run the following command:

.. code-block:: console

    python3 -m venv <path/to/new/virtual/environment>

To activate the virtual environment, run the following command:

(In Linux/MacOS)

.. code-block:: console

    source <path/to/new/virtual/environment>/bin/activate

(In Windows)

.. code-block:: console

    <path/to/new/virtual/environment>/Scripts/activate

To deactivate the virtual environment, run the following command:

.. code-block:: console

    deactivate

A requirements.txt file is provided in the repository for (most of) the required dependencies. To install the dependencies, run the following command:

.. code-block:: console

    pip install -r requirements.txt

Verify Django installation by going into python terminal:

.. code-block:: python

    >>> import django
    >>> print(django.get_version())


SQLite3 is **not directly available through pip** (in Windows at least). Install SQLite3 from [official website](https://www.sqlite.org/download.html).

For developers
--------------

The ``main`` branch is the stable branch. 

The ``dev`` branch is the develop branch where the latest changes are pushed.

The ``pyproject.toml`` file is a configuration for the tidy_interface package. 

The ``readthedocs-pyproject.toml`` file is a configuration for the documentation.

The ``MANIFEST.in`` file is a configuration for the package to include extra files such as example data.
Inside the MANIFEST.in file, specify the .csv file (or any other files you want to include) using the include directive.

Please maintain a clean file structure as the following:

.. code-block:: console

    tidy_interface/
    |-- tidy_interface/
    |   |-- __init__.py
    |   |-- signal_manager.py
    |   |-- other_potential_modules.py
    |   |-- examples/
    |       |-- example.py
    |   |-- example_data/
    |   |   |-- example_file.csv
    |-- docs/
    |-- prototyping/
    |-- tests/
    |-- README.rst
    |-- LICENSE
    |-- setup.py
    |-- pyproject.toml
    |-- readthedocs-pyproject.toml
    |-- requirements.txt
    |-- MANIFEST.in
    |-- dist/
    |   |-- tidy_interface-0.1.1.tar.gz
    |-- tidy_interface.egg-info/
    |   |-- ...
    |-- .gitignore

To install an unofficial version of the package, e.g., the current ``dev`` branch, run the following command:

.. code-block:: console

    git checkout dev
    python3 setup.py sdist
    pip install dist/tidy_interface-x.x.x.tar.gz

The ``x.x.x`` is the auto-generated version number.

.. |docs| image:: https://readthedocs.org/projects/tidy-interface/badge/?version=stable
    :target: https://tidy-interface.readthedocs.io/en/latest/?badge=stable
    :alt: Documentation Status (stable)