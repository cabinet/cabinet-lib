#!/usr/bin/env python
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.md').read()
# history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open('requirements.txt').read().splitlines()

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='cabinet',
    version='0.1.0',
    description=('A collab password manager library that uses gpg to store '
                 'your sensitive data.'),
    # long_description=readme + '\n\n' + history,
    long_description=readme,
    author='Ivan Bienco',
    author_email='ivanalejandro0@gmail.com',
    url='https://github.com/ivanalejandro0/cabinet',
    packages=[
        'cabinet',
    ],
    package_dir={'cabinet':
                 'cabinet'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='cabinet',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
