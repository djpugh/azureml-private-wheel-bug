from setuptools import find_packages, setup


kwargs = dict(name='testpackage',
              version='0.0.1',
              packages=find_packages('src'),
              package_dir={'': 'src'},
              requires=[],
              provides=['testpackage'],
              description="Test package",
              long_description="Test package",
              )

setup(**kwargs)
