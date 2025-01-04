from setuptools import find_packages
from setuptools import setup

setup(
    name='aura_controller',
    version='0.0.0',
    packages=find_packages(
        include=('aura_controller', 'aura_controller.*')),
)
