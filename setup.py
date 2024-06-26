from setuptools import setup, find_packages
import glob
import os
import pkg_resources

from hedgehog import __version__, _program

setup(name='hedgehog',
      version=__version__,
      packages=find_packages(),
      scripts=['hedgehog/scripts/parallel_align.smk',
                'hedgehog/scripts/hedge_lineage_set.smk'],
      package_data={"hedgehog":["data/*"]},
      install_requires=[
            "biopython>=1.74",
            'pandas>=1.0.1',
            "wheel>=0.34",
            'joblib>=0.11',
            'scikit-learn==1.2.2',
            "PuLP>=2"        
            ],
      description='',
      url='https://github.com/aineniamh/hedgehog',
      author='Aine OToole',
      author_email='aine.otoole@ed.ac.uk',
      entry_points="""
      [console_scripts]
      {program} = hedgehog.command:main
      """.format(program = _program),
      include_package_data=True,
      keywords=[],
      zip_safe=False)
