Usage
=====

.. _installation:

Installation
------------

To use tiny_interface, first install it using pip (TBD):

.. code-block:: console

   (.venv) $ pip install tiny_interface

The above python package installation is TBD. For now, you can install the package by cloning the repository and running the following command from the root directory of the repository:

This tool uses Python, Django, SQLite3, pyyaml for database management. To install dependencies, it is recommended to first create a virtual environment. To create a virtual environment, run the following command:

.. code-block:: console

   (.venv) $ python3 -m venv <path/to/new/virtual/environment>

To activate the virtual environment, run the following command (in Linux or MacOS):

.. code-block:: console

    (.venv) $ source <path/to/new/virtual/environment>/bin/activate

In Windows, run the following command:

.. code-block:: console

    <path/to/new/virtual/environment>/Scripts/activate

To deactivate the virtual environment, run the following command:

.. code-block:: console

    deactivate

A requirements.txt file is provided in the repository. To install the dependencies, run the following command:

.. code-block:: console

    pip install -r requirements.txt

Verify Django installation by going into python terminal:

.. code-block:: python

    >>> import django
    >>> print(django.get_version())

SQLite3 is not directly available through pip. Install SQLite3 from [official website](https://www.sqlite.org/download.html) for viewing the data tables.



Creating interface signal database
----------------------------------

To create a database of interface signals, use the ``signalManager.create_database()`` function.

For example:

.. code-block:: python

    >>> from tiny_interface import signalManager
    >>> mgr = signalManager()
    >>> mgr.create_database()