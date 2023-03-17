
from setuptools import setup, find_packages # automatically finds all the packages exist in folders having __init__.py

setup(
    name ='src', 
    version = '0.01',
    description = "Its a wine quality ML implementation with mlops",
    author = "Malleswari Gelli",
    packages = find_packages(), # finds all packages exist in crrent working directory where ever __init__.py file is there
    licence = "MIT"
    
)