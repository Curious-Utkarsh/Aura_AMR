from setuptools import find_packages
from setuptools import setup

setup(
    name='aura_mapping',
    version='0.0.0',
    packages=find_packages(
        include=('aura_mapping', 'aura_mapping.*')),
)
