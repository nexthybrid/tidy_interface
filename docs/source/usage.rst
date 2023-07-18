Usage
=====

.. _installation:

Installation
------------

To use tiny_interface, first install it using pip (TBD):

.. code-block:: console

   (.venv) $ pip install tiny_interface

Creating interface signal database
----------------------------------

To create a database of interface signals, use the ``signalManager.create_database()`` function.

For example:

>>> from tiny_interface import signalManager
>>> mgr = signalManager()
>>> mgr.create_database()