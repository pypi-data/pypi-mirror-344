from setuptools import setup, find_packages

setup(
    name='principal_portfolios',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[],
    author='Amin Izadyar',
    author_email='a.izadyar23@imperial.ac.uk',
    description='Developed a package for the Prinipal Portfolios approach',
    url='https://github.com/aminizadyar/Principal-Portfolios', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)