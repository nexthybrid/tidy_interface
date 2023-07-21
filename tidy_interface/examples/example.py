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