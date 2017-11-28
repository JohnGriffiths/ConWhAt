#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup(name='conwhat',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='python library for connectome-based white matter atlas analyses in neuroimaging',
      long_description='python library for connectome-based white matter atlas analyses in neuroimaging',
      keywords='white matter, tractography, MRI, DTI, diffusion, python',
      author='John David Griffiths',
      author_email='j.davidgriffiths@gmail.com',
      url='https://github.com/JohnGriffiths/conwhat',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      install_requires=['numpy',  'setuptools', 'pandas', 'nibabel', 'sklearn', 'nilearn',
                        'dipy', 'joblib', 'matplotlib', 'pyyaml', 'networkx', 'indexed_gzip'],
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Software Development',
          'Topic :: Scientific/Engineering',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
      ],
      entry_points={
          "console_scripts": [
              "conwhat=conwhat.__main__:main",
          ]
      }
      )
