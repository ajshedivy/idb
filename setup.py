from setuptools import setup, find_packages 

setup(
    name="ibmi_db",
    version="0.0.2",
    author="Adam Shedivy",
    long_description="A package for connecting to a remote database using SSH.",
    package_dir={"": "src"},
    install_requires=["paramiko", "enum34"],
    url='https://github.com/ajshedivy/idb'
)