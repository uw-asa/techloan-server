from setuptools import find_packages, setup

setup(
    name="techloan-server",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'coreapi',
        'Django',
        'djangorestframework>=3.4.0',
        'pymssql',
        'python-dateutil',
    ],
)
