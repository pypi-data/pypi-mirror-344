
from setuptools import setup, find_packages

setup(
    name='glair',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.15.0',
        'numpy>=1.26.0',
        'nibabel>=5.3.2',
        'matplotlib>=3.9.2',
        'scipy>=1.13.1',
        'keras>=3.9.1'
    ],
)