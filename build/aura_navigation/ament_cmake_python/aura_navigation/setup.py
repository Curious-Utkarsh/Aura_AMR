from setuptools import find_packages
from setuptools import setup

setup(
    name='aura_navigation',
    version='0.0.0',
    packages=find_packages(
        include=('aura_navigation', 'aura_navigation.*')),
)
