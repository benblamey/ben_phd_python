__author__ = "ben-laptop"
__date__ = "$04-Feb-2015 09:46:20$"

from setuptools import setup, find_packages

setup (
       name='ben_phd_python',
       version='0.1',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['foo>=3'],

       # Fill in these to make your Egg ready for upload to
       # PyPI
       author='ben-laptop',
       author_email='',

       summary='Just another Python package for the cheese shop',
       url='',
       license='',
       long_description='Long description of the package',

       # could also include long_description, download_url, classifiers, etc.

  
       )