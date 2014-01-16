import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='chocula',
    version='0.1',
    description='Tools for counting experiments.',
    long_description=read('README.md'),
    author='Andy Mastbaum',
    author_email='mastbaum@hep.upenn.edu',
    scripts=['bin/chocula'],
    packages=find_packages(),
    package_data={'chocula.data': ['*.csv']}
)

