from setuptools import setup, find_packages
setup(
    name="techloan-server",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Django',
        'pymssql',
    ],
)
