#!/usr/bin/env python3

from setuptools import find_packages, setup

with open('README.rst', 'r') as file:
    long_description = file.read()

setup(
    name='mcp4161',
    version='0.0.0.dev3',
    description='A Python driver for Microchip Technology MCP4161 7/8-Bit Single/Dual SPI Digital POT with Non-Volatile Memory',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/blueskysolarracing/mcp4161',
    author='Blue Sky Solar Racing',
    author_email='blueskysolar@studentorg.utoronto.ca',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords=[
        'python',
    ],
    project_urls={
        'Documentation': 'https://mcp4161.readthedocs.io/en/latest/',
        'Source': 'https://github.com/blueskysolarracing/mcp4161',
        'Tracker': 'https://github.com/blueskysolarracing/mcp4161/issues',
    },
    packages=find_packages(),
    install_requires=[
         'python-periphery>=2.4.1,<3',
    ],
    python_requires='>=3.11',
    package_data={'mcp4161': ['py.typed']},
)
