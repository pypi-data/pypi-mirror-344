from setuptools import setup, find_packages

setup(
    name='autoprocessor',
    version='0.4.0',
    packages=find_packages(where='src'),  # This tells setuptools to look in the 'src' folder
    package_dir={'': 'src'},  # This tells setuptools that the packages are under 'src'
    install_requires=[
        # Add your dependencies here
    ],
)
