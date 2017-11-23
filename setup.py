#!/usr/bin/env python3
from setuptools import setup, find_packages

version_string = "1.0.0"

packages = find_packages(
    exclude=[]
)

setup(
    name='multiplication-test-generator',
    version=version_string,
    description="Generator of multiplication table tests for Basic School",
    author='Jakub Zeman',
    author_email='jakubzeman@gmail.com',
    url='https://github.com/jakubzeman/multiplication-table-test-generator',
    keywords=["multiplication", "basic school"],
    packages=packages,
    install_requires=["click"],
    zip_safe=True,
    scripts=['bin/multiplication-test-generator', 'bin/multiplication-test-generator.bat'],
    classifiers=[]
)
