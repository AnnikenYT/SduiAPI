from setuptools import setup

setup(
   name='sdui_api_wrapper',
   version='0.5',
   description='Get preparsed data from the sdui api',
   author='AnnikenYT + Vob',
   author_email='anniken@mooonshine.net',
   packages=['sdui_api_wrapper'],  #same as name
   install_requires=['wheel', 'bar', 'greek', 'colorama'], #external packages as dependencies
)