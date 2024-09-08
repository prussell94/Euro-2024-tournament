from setuptools import setup, find_packages

setup(
    name='euro_2024_tournament',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'pandas',
        # List other dependencies here
    ],
    author='Your Name',
    description='Euro 2024 Tournament Tournament',
    url='https://github.com/prussell94/Euro-2024-tournament',
)