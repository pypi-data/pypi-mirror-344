from setuptools import setup, find_packages

setup(
    name='autoprocessor',
    version='0.5.0',
    packages=find_packages(where='src'),  # Ensure packages are found in 'src'
    package_dir={'': 'src'},  # Tell setuptools where to find the packages
    include_package_data=True,  # Ensure non-Python files are included
    install_requires=[
        # Add any dependencies here
    ],
)
