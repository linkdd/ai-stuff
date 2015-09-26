#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='linkai',
    version='0.1',
    license='MIT',

    author='David Delassus',
    author_email='david.jose.delassus@gmail.com',
    description='Artificial intelligence tools',
    url='https://github.com/linkdd/ai-stuff',
    keywords=['artificial', 'intelligence', 'linkai'],
    classifiers=[],

    packages=find_packages(),
    install_requires=[
        'b3j0f.utils',
        'b3j0f.conf',
    ]
)
