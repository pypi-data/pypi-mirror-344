from setuptools import setup, find_packages

setup(
    name='autoprocessor',
    version='0.7.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,  # This ensures non-Python files are included
    package_data={
        '': ['src/checkthisout/*.ipynb', 'src/checkthisout/*.csv', 'src/checkthisout/*.pdf'],  # Specify additional files
    },
    install_requires=[
        # Add any dependencies here
    ],
)
