from setuptools import setup, find_packages

setup(
    name='publish_to_pypi_again',
    version='0.6',
    license='MIT',
    author="SpiralTrain",
    author_email='spiraltrain@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='example project',
    install_requires=[
          'scikit-learn',
          'numpy',
      ],
)
