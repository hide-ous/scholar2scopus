#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'scholarly~=1.5.1',
    'pandas~=1.3.5',
    'tqdm~=4.62.3',
    'thefuzz~=0.19.0'
]

test_requirements = []

setup(
    author="Mattia Samory",
    author_email='mattia.samory@gesis.org',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Find citations that are on Scholar but not Scopus",
    entry_points={
        'console_scripts': [
            'scholar2scopus=scholar2scopus.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme,
    include_package_data=True,
    keywords='scholar2scopus',
    name='scholar2scopus',
    packages=find_packages(include=['scholar2scopus', 'scholar2scopus.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hide-ous/scholar2scopus',
    version='0.0.1',
    zip_safe=False,
)
