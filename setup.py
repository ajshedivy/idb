from setuptools import setup, find_packages 

setup(
    name="ibmidb",
    version="0.0.2",
    author="Adam Shedivy",
    long_description="A package for connecting to a remote database using SSH.",
    package_dir={"": "src"},
    install_requires=["paramiko"],
    url='https://github.com/ajshedivy/idb'
)