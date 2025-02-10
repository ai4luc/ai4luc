
import os

try:
    os.system("python -m ensurepip --upgrade")
    os.system("python -m pip install --upgrade setuptools")
except:
    pass

from setuptools import setup, find_packages

req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
if os.path.exists(req_file):
    with open(req_file) as f:
        requirements = f.read().splitlines()
else:
    requirements = []

with open(os.path.join('ai4luc', '_version.py')) as f:
    version_line = next(filter(lambda line: line.startswith('__version__'), f))
    __version__ = version_line.split('=')[-1]

setup(
    name="ai4luc",
    version=__version__.strip().strip('"'),
    author="Miranda, Mateus de S. and Santiago Junior, Valdivino Alexandre de and Korting, Thales Sehn",
    author_email="mateus.miranda@inpe.br",
    description="A Python package for classification of land use and land cover",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ai4luc/ai4luc",
    packages=find_packages(),
    install_requires=requirements,
    license="LICENSE",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Land use and land cover",
    ]
)