# coding: utf-8
"""
Setup module.
"""
from __future__ import absolute_import

# Standard imports
import sys

# External imports
from setuptools import find_packages
from setuptools import setup


# Run setup
setup(
    name='AoikDynamicClosure',

    version='0.1.0',

    description=(
        'Enable dynamic binding of closure variables.'
    ),

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikDynamicClosure>`_""",

    url='https://github.com/AoiKuiyuyou/AoikDynamicClosure',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    keywords='closure',

    package_dir={
        '': 'src'
    },

    packages=find_packages('src'),

    include_package_data=True,

    install_requires=[
        'byteplay >= 0.2' if sys.version_info[0] == 2
        else 'byteplay3 >= 3.5.0',
    ],
)
