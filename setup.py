import os
from setuptools import setup, find_packages

# Temporarily disable build isolation to disable documentation build
# os.environ['PIP_NO_BUILD_ISOLATION'] = '0'

setup(
    name='tidy_interface',
    version='0.1.1',
    author='Tong Zhao',
    author_email='zhao.1991@osu.edu',
    description='An interface signal management tool.',
    long_description='is a signal interface management tool for managing interface signals across different versions.',
    packages=find_packages(),
    package_data={
        'tidy_interface': ['example_data/*'],
    },
    install_requires=[
        'pyyaml',
        # 'pysqlite3', # removed because Windows does not support this, need to manually install sqlite3
    ],
)