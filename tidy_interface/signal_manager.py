import sqlite3
import csv
import uuid
import datetime
import yaml

class SignalManager:
    """
    A class that manages the database with the Signals and SignalVersions table.
    """

    def __init__(self, db_file):
        """
        Initialize the SignalManager.

        Args:
            db_file (str): The path to the SQLite database file.
        """
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """
        Establish a connection to the database.
        """
        self.conn = sqlite3.connect(self.db_file)

    def disconnect(self):
        """
        Disconnect from the database.
        """
        if self.conn:
            self.conn.close()

    def create_database(self):
        """
        Create the database with the Signals and SignalVersions table.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS Signals(
                uuid TEXT PRIMARY KEY,
                latest_signal_name TEXT,
                creation_info TEXT,
                creation_date TEXT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS SignalVersions(
                signal_uuid TEXT,
                signal_name TEXT,
                unit TEXT,
                default_value TEXT,
                size TEXT,
                software_version TEXT,
                FOREIGN KEY (signal_uuid) REFERENCES Signals(uuid)
            )
        ''')

        self.conn.commit()
        self.disconnect()
        print("Database created successfully.")

    def import_data(self, csv_file, software_version):
        """
        Import data into the database using a CSV file.
        The CSV file should have the following columns:
            - signal name
            - unit
            - default value
            - size
        The CSV file should have a header row.

        Args:
            csv_file (str): The path to the CSV file.
            software_version (str): The software version associated with the data.
        """
        self.connect()
        c = self.conn.cursor()

        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)

            for row in reader:
                signal_uuid = self.add_uuid(row['signal name'], 'import', csv_file, software_version)
                self.add_signal_version(signal_uuid, row['signal name'], row['unit'], row['default value'], row['size'], software_version)

        print("Data imported successfully.")

    def add_uuid(self, signal_name, creation_type='manual', csv_file=None, software_version=None):
        """
        Add a UUID to the Signals table. There are two options for the creation_type:
            - manual: manually created
            - import: imported from a CSV file, also requires the CSV filename and software version

        Args:
            signal_name (str): The signal name.
            creation_type (str): The type of creation. Defaults to 'manual'.
            csv_file (str): The path to the CSV file. Defaults to None.
            software_version (str): The software version associated with the data. Defaults to None.

        Returns:
            str: The generated UUID.
        """
        signal_uuid = str(uuid.uuid4())
        self.connect()
        c = self.conn.cursor()

        # use a switch to determine the creation_info based on the creation_type
        if creation_type == 'manual':
            creation_info = 'Manually created'
            print("Mannually adding a UUID to the Signals table for signal " + signal_name + ".")
        elif creation_type == 'import':
            creation_info = 'Imported from CSV file ' + csv_file + ' with version ' + software_version
            print("Adding a UUID to the Signals table for signal " + signal_name + " imported from CSV file " + csv_file + " with version " + software_version + ".")

        c.execute('INSERT INTO Signals (uuid, latest_signal_name, creation_info, creation_date) VALUES (?, ?, ?, ?)', \
                  (signal_uuid, signal_name, creation_info, datetime.datetime.now()))

        self.conn.commit()
        self.disconnect()
        return signal_uuid

    def add_signal_version(self, signal_uuid, signal_name, unit, default_value, size, software_version):
        """
        Add a signal version entry to the SignalVersions table.

        Args:
            signal_uuid (str): The UUID of the signal.
            signal_name (str): The signal name.
            unit (str): The unit of the signal.
            default_value (str): The default value of the signal.
            size (int): The size of the signal.
            software_version (str): The software version associated with the signal.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute('''
            INSERT INTO SignalVersions (signal_uuid, signal_name, unit, default_value, size, software_version)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (signal_uuid, signal_name, unit, default_value, size, software_version))

        self.conn.commit()
        self.disconnect()
        print('Signal version entry added successfully for signal ' + signal_name + ' with UUID ' + signal_uuid + '.')

    def get_uuid(self, signal_name):
        """
        Get the UUID of a signal given its latest_signal_name.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute('''
            SELECT uuid
            FROM Signals
            WHERE latest_signal_name = ?
            ''', (signal_name,))
        uuid = c.fetchone()

        self.disconnect()

        if uuid:
            return uuid[0]
        else:
            return None

    def export_signals(self, software_version, output_file):
        """
        Export the signals of a specific software version to a YAML file.

        Args:
            software_version (str): The software version.
            output_file (str): The path to the output YAML file.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute('''
            SELECT s.uuid, sv.signal_name, sv.unit, sv.default_value, sv.size
            FROM Signals s
            INNER JOIN SignalVersions sv ON s.uuid = sv.signal_uuid
            WHERE sv.software_version = ?
        ''', (software_version,))
        rows = c.fetchall()

        signals = []
        for row in rows:
            signal = {
                'uuid': row[0],
                'signal_name': row[1],
                'unit': row[2],
                'default_value': row[3],
                'size': row[4]
            }
            signals.append(signal)

        with open(output_file, 'w') as f:
            yaml.dump(signals, f)

        self.disconnect()
        print(f"Signals exported to {output_file} successfully.")

    def export_signals_csv(self, software_version, output_file):
        """
        Export the signals of a specific software version to a CSV file.

        Args:
            software_version (str): The software version.
            output_file (str): The path to the output CSV file.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute('''
            SELECT s.uuid, sv.signal_name, sv.unit, sv.default_value, sv.size
            FROM Signals s
            INNER JOIN SignalVersions sv ON s.uuid = sv.signal_uuid
            WHERE sv.software_version = ?
        ''', (software_version,))
        rows = c.fetchall()

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['uuid', 'signal_name', 'unit', 'default_value', 'size'])
            writer.writerows(rows)

        self.disconnect()
        print(f"Signals exported to {output_file} successfully.")
