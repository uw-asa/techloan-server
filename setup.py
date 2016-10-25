from setuptools import setup, find_packages
setup(
    name="techloan-server",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Django',
        'djangorestframework>=3.4.0',
        'pymssql',
    ],
)
