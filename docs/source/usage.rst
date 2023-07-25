Usage
=====

.. _installation:

Installation
------------

To use tiny_interface, first install it using pip (TBD):

.. code-block:: console

   (.venv) $ pip install tiny_interface

The above python package installation is TBD (need to push to PyPl). For now, you can install the package by cloning the repository and running the following command from the root directory of the repository:

.. code-block:: console

    (.venv) $ git clone https://github.com/nexthybrid/tidy_interface.git
    (.venv) $ cd tidy_interface
    (.venv) $ python3 -m setup.py sdist
    (.venv) $ python3 -m pip install dist/tiny_interface-x.x.x.tar.gz

This tool uses Python, Django, SQLite3, pyyaml for database management. While pyyaml is included in the package installation, sqlite3 is not, as it is not directly available in Windows through pip. SQLite3 can be installed from [official website](https://www.sqlite.org/download.html).

To install dependencies, it is recommended to first create a virtual environment. To create a virtual environment, run the following command:

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

Import signals from CSV file
----------------------------

To import signals from a CSV file, use the ``signalManager.import_data()`` function.

For example:

.. code-block:: python

    >>> from tiny_interface import signalManager
    >>> mgr = signalManager()
    >>> mgr.import_data(csv_file, software_version)

The ``csv_file`` argument is the path to the CSV file containing the signals. The ``software_version`` argument is the version of the software for which the signals are being imported.

A sample CSV file is provided in the package. The CSV file has the following columns: signal name,unit,default value,size.

The code below performs the following tasks:

1. Creates a database of interface signals.
2. Imports signals from the sample CSV file.
3. Manually add five uuids to the Signals table.
4. Manually insert a few signal versions entries into the database.
5. Export the database to a CSV file.
6. Export the database to a YAML file.

.. code-block:: python

    # Example usage of the SignalManager class.
    # This usage resembles the prototype scripts in the sql.ipynb notebook, but is more concise with a class.
    import os
    import pkg_resources
    from tidy_interface.signal_manager import SignalManager


    def get_example_data_file():
        package_name = 'tidy_interface'
        filename = 'example_data/signals_from_csv.csv'

        file_path = pkg_resources.resource_filename(package_name, filename)
        return file_path


    db_file = 'signals.db'
    mgr = SignalManager(db_file)

    mgr.create_database()
    # data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "example_data", "signals_from_csv.csv")
    data_file_path = get_example_data_file()
    mgr.import_data(data_file_path, '1.0.0')

    # Manually add five uuids to the Signals table
    for i in range(5):
        mgr.add_uuid(f'signal_{i}')

    # Manually insert a few signal versions entries into the database
    uuid_0 = mgr.get_uuid('signal_0')
    uuid_1 = mgr.get_uuid('signal_1')

    # software version 1.0.0
    mgr.add_signal_version(uuid_0, 'signal_0_name_v1p0', 'kph', 1, '[1]', '1.0.0')
    mgr.add_signal_version(uuid_1, 'signal_1_name_v1p0', 'ampere', 0, '[1]', '1.0.0')

    # software version 1.1.0
    mgr.add_signal_version(uuid_0, 'signal_0_name_v1p1', 'kph', 100, '[1]', '1.1.0')
    mgr.add_signal_version(uuid_1, 'signal_1_name_v1p1', 'ampere', 10, '[1]', '1.1.0')

    mgr.export_signals('1.0.0', 'signals.yaml')
    mgr.export_signals_csv('1.1.0', 'signals.csv')

