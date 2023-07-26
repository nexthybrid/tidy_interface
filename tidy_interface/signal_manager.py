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
        self.SignalVersions_columns = [
            "signal_uuid",
            "signal_name",
            "unit",
            "default_value",
            "size",
            "software_version",
        ]

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
        By default, the Signals table has the following columns:
            - uuid: the UUID of the signal
            - latest_signal_name: the latest signal name
            - creation_info: the creation information
            - creation_date: the creation date
        By default, the SignalVersions table has the following columns:
            - signal_uuid: the UUID of the signal, which is linked to the Signals table
            - signal_name: the signal name
            - unit: the unit of the signal
            - default_value: the default value of the signal
            - size: the size of the signal
            - software_version: the software version associated with the signal
        The columns in the SignalVersions table are customizable. But the first one must be the signal_uuid, which is linked to the Signals table. And the last one must be the software_version.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS Signals(
                uuid TEXT PRIMARY KEY,
                latest_signal_name TEXT,
                creation_info TEXT,
                creation_date TEXT
            )
        """
        )

        # c.execute('''
        #     CREATE TABLE IF NOT EXISTS SignalVersions(
        #         signal_uuid TEXT,
        #         signal_name TEXT,
        #         unit TEXT,
        #         default_value TEXT,
        #         size TEXT,
        #         software_version TEXT,
        #         FOREIGN KEY (signal_uuid) REFERENCES Signals(uuid)
        #     )
        # ''')

        # Create a string with placeholders for the column names
        placeholders = ", ".join(
            ["{} TEXT".format(col) for col in self.SignalVersions_columns]
        )
        # Create the SQL query dynamically using string formatting
        query = f"""
            CREATE TABLE IF NOT EXISTS SignalVersions (
                {placeholders},
                FOREIGN KEY ({self.SignalVersions_columns[0]}) REFERENCES Signals({self.SignalVersions_columns[0]})
            )
        """
        # Execute the query to create the table
        c.execute(query)

        self.conn.commit()
        self.disconnect()
        print("Database created successfully.")

    def delete_signalVersions_table(self):
        """
        Delete the SignalVersions table.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute("DROP TABLE IF EXISTS SignalVersions")

        self.conn.commit()
        self.disconnect()
        print("SignalVersions table deleted successfully.")

    def reload_database(self):
        """
        Reload the database by deleting the SignalVersions table and creating it again.
        """
        self.delete_signalVersions_table()
        self.create_database()

    def clear_signalVersions_columns(self):
        """
        Clear the column definitions of the SignalVersions table.
        """
        self.SignalVersions_columns = []

    def add_signalVersions_column(self, column_name):
        """
        Add a column to the SignalVersions table.

        Args:
            column_name (str): The column name.
        """
        self.SignalVersions_columns.append(column_name)

    def reset_signalVersions_columns(self):
        """
        Reset the column definitions of the SignalVersions table so it only has the essentials.
        The user is responsible for adding the signal_version column at the very end.
        """
        self.SignalVersions_columns = [
            "signal_uuid",
        ]

    def import_data(self, csv_file, software_version):
        """
        Import data into the database using a CSV file.
        The CSV file should have the following columns (for the default SignalVersions table):
            - signal_name
            - unit
            - default_value
            - size
        The CSV file should have a header row.

        If the SignalVersions table has been customized, the CSV file should have a list of columns
        that match the SignalVersions table, but without the the signal_uuid and software_version columns.

        The signal_uuid will be generated automatically. The software_version will be an input.

        Args:
            csv_file (str): The path to the CSV file.
            software_version (str): The software version associated with the data.
        """
        self.connect()
        c = self.conn.cursor()

        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                signal_uuid = self.add_uuid(
                    row["signal_name"], "import", csv_file, software_version
                )
                args = [value for value in row.values()]
                args.insert(0, signal_uuid)
                args.append(software_version)
                self.add_signal_version(*args)

        print("Data imported successfully.")

    def add_uuid(
        self, signal_name, creation_type="manual", csv_file=None, software_version=None
    ):
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
        if creation_type == "manual":
            creation_info = "Manually created"
            print(
                "Mannually adding a UUID to the Signals table for signal "
                + signal_name
                + "."
            )
        elif creation_type == "import":
            creation_info = (
                "Imported from CSV file "
                + csv_file
                + " with version "
                + software_version
            )
            print(
                "Adding a UUID to the Signals table for signal "
                + signal_name
                + " imported from CSV file "
                + csv_file
                + " with version "
                + software_version
                + "."
            )

        c.execute(
            "INSERT INTO Signals (uuid, latest_signal_name, creation_info, creation_date) VALUES (?, ?, ?, ?)",
            (signal_uuid, signal_name, creation_info, datetime.datetime.now()),
        )

        self.conn.commit()
        self.disconnect()
        return signal_uuid

    def add_signal_version(self, *args):
        """
        Add a signal version entry to the SignalVersions table.

        Args (For default database schema):
            signal_uuid (str): The UUID of the signal.

            (The following are default values, but can be changed)
            signal_name (str): The signal name.
            unit (str): The unit of the signal.
            default_value (str): The default value of the signal.
            size (int): The size of the signal.

            (The following are required)
            software_version (str): The software version associated with the signal.
        """
        self.connect()
        c = self.conn.cursor()

        # A Placeholder for the column names
        placeholders = ", ".join(
            ["{}".format(col) for col in self.SignalVersions_columns]
        )

        question_marks = ", ".join(["?" for _ in self.SignalVersions_columns])

        query = f"""
            INSERT INTO SignalVersions ({placeholders})
            VALUES ({question_marks})
        """

        list_of_values = [value for value in args]
        # Turn the list into a tuple
        tuple_of_values = tuple(list_of_values)

        c.execute(
            query,
            tuple_of_values,
        )

        self.conn.commit()
        self.disconnect()
        print(
            "Signal version entry added successfully for signal "
            + self.SignalVersions_columns[1]
            + " with UUID "
            + self.SignalVersions_columns[0]
            + "."
        )

    def get_uuid(self, signal_name):
        """
        Get the UUID of a signal given its latest_signal_name.
        """
        self.connect()
        c = self.conn.cursor()

        c.execute(
            """
            SELECT uuid
            FROM Signals
            WHERE latest_signal_name = ?
            """,
            (signal_name,),
        )
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

        placeholder = ", ".join(
            ["sv.{}".format(col) for col in self.SignalVersions_columns]
        )

        query = f"""
            SELECT {placeholder}
            FROM Signals s
            INNER JOIN SignalVersions sv ON s.uuid = sv.signal_uuid
            WHERE sv.software_version = ?
        """

        c.execute(
            query,
            (software_version,),
        )

        rows = c.fetchall()

        # Assuming c.description is available and it contains column names
        columns = [column[0] for column in c.description]

        # Convert rows to list of dictionaries
        data = [dict(zip(columns, row)) for row in rows]

        # Export to YAML
        with open("output.yaml", "w") as f:
            yaml.dump(data, f)

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

        placeholder = ", ".join(
            ["sv.{}".format(col) for col in self.SignalVersions_columns]
        )

        query = f"""
            SELECT {placeholder}
            FROM Signals s
            INNER JOIN SignalVersions sv ON s.uuid = sv.signal_uuid
            WHERE sv.software_version = ?
        """

        c.execute(
            query,
            (software_version,),
        )

        rows = c.fetchall()

        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            column_names = self.SignalVersions_columns
            writer.writerow(column_names)
            writer.writerows(rows)

        self.disconnect()
        print(f"Signals exported to {output_file} successfully.")

    def export_signals_csv_all(self, output_file):
        """
        Export all signals to a CSV file.

        Args:
            output_file (str): The path to the output CSV file.
        """
        self.connect()
        c = self.conn.cursor()

        placeholder = ", ".join(
            ["sv.{}".format(col) for col in self.SignalVersions_columns]
        )

        query = f"""
            SELECT {placeholder}
            FROM Signals s
            INNER JOIN SignalVersions sv ON s.uuid = sv.signal_uuid
        """

        c.execute(
            query,
        )

        rows = c.fetchall()

        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            column_names = self.SignalVersions_columns
            writer.writerow(column_names)
            writer.writerows(rows)

        self.disconnect()
        print(f"Signals exported to {output_file} successfully.")
