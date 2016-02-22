from setuptools import setup, find_packages
setup(
    name = "open_data",
    version = "0.0.1",
    packages = find_packages(),
    author='Nick Gustafson',
    author_email='njgustafson@gmail.com',
    url='https://github.com/oeuf/open_data',
    description='scratchpaad code for accessing data on socrata',
    install_requires=[
        'gevent',
        'PyYAML',
        'retrying',
        'sodapy',
    ],
)
