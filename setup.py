from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), 'r') as f:
    long_description = f.read()

setup(
    name='Terrarium',
    version='0.2.0dev1',
    description='Hospitable Runtime Environments',
    long_description=long_description,

    url='https://github.com/artPlusPlus/Terrarium',

    author='Matt Robinson',
    author_email='matt@technicalartisan.com',

    license='MIT',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',
        'Topic :: System',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7'
    ],

    keywords='runtime environment',

    packages=find_packages(),

    install_requires=[],

    extras_require={
        'test': ['py.test']
    }
)
