from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as buff:
    long_description = buff.read()

setup(
    name='callisto',
    version='0.7',
    description='Create jupyter kernels from virtual environments',
    long_description=long_description,
    author='Colin Carroll',
    author_email='colcarroll@gmail.com',
    url='https://github.com/ColCarroll/callisto',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['test']),
    install_requires=[
        'Click',
        'ipykernel'
    ],
    include_package_data=True,
    entry_points='''
    [console_scripts]
    callisto=callisto:cli
    ''',
)
