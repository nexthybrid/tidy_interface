Data Tables
==================

SQL Tables
----------

The following tables are used to store the data:

``Signals``: This table stores the signals that are related to interfaces. This table is indexed by UUIDs generated automatically during initial addition of the signal to the database. The table has the following columns:

* ``uuid``: The UUID of the signal. This is the primary key of the table.
* ``latest_signal_name``: the latest signal name
* ``creation_info``: the creation information
* ``creation_date``: the creation date

``SignalVersions``: This table stores various attributes of each signal for each software version. The table has the following default columns:
* ``signal_uuid``: the UUID of the signal, which is linked to the Signals table
* ``signal_name``: the signal name
* ``unit``: the unit of the signal
* ``default_value``: the default value of the signal
* ``size``: the size of the signal
* ``software_version``: the software version associated with the signal

.. note:: 
    The columns of the ``SignalVersions`` table is customizable. But the default columns are the ones listed above. 
    The ``signal_uuid`` column and the ``software_version`` column are required. 
    The ``signal_uuid`` column is linked to the ``Signals`` table. 
    The ``software_version`` column is used to identify what version any entry in this table belongs to.
    Also, the ``signal_uuid`` column is automatically added after resetting the SignalVersions table. 
    The ``software_version`` column needs to be added by the user after resetting the SignalVersions table, **at the end** of the list of columns.