from setuptools import setup, find_packages 

setup(
    name='lavista',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
        # For example:
        'numpy',            
        'pandas',
        'scikit-learn',
        'matplotlib',
    ],
)        