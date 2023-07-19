tidy_interface
==============

[![Documentation Status](https://readthedocs.org/projects/tidy-interface/badge/?version=latest)](https://tidy-interface.readthedocs.io/en/latest/?badge=latest)
**tidy_interface** is a signal interface management tool for managing interface signals across different versions. Detailed documentation can be found [here](https://tidy-interface.readthedocs.io/en/).

Dependencies
------------

This tool uses Python, Django, SQLite3, pyyaml for database management. To install dependencies, it is recommended to first create a virtual environment. To create a virtual environment, run the following command:
```bash
python3 -m venv <path/to/new/virtual/environment>
```
To activate the virtual environment, run the following command:
```bash
source <path/to/new/virtual/environment>/bin/activate
```
To deactivate the virtual environment, run the following command:
```bash
deactivate
```

A requirements.txt file is provided in the repository. To install the dependencies, run the following command:
```bash
pip install -r requirements.txt
```
Verify Django installation by going into python terminal:
```python
>>> import django
>>> print(django.get_version())
```

SQLite3 is not directly available through pip. Install SQLite3 from [official website](https://www.sqlite.org/download.html) for viewing the data tables.

