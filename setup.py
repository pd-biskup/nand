from setuptools import setup, find_packages


setup(name='nand',
      version='indev',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'nand = nand.__main__:main'
          ]
      })
