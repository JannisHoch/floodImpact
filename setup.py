#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

# requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jannis M. Hoch",
    author_email='j.m.hoch@uu.nl',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Applying network modelling to hydrology.",
    entry_points={
        'console_scripts': ['floodimpact=flood_impact.scripts.click_functions:cli'],
    },
    install_requires=requirements,
    license="MIT",
    long_description=readme,
    include_package_data=True,
    keywords='flood impact, population exposure, flood risk',
    name='floodimpact',
    packages=find_packages(include=['flood_impact', 'flood_impact.*'], exclude=['data', 'pics,']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='',
    version='0.2.0',
    zip_safe=False,
)
