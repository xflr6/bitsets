# setup.py

import io
from setuptools import setup, find_packages

setup(
    name='bitsets',
    version='0.8.dev0',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Ordered subsets over a predefined domain',
    keywords='ordered set finite immutable bit string array map field',
    license='MIT',
    url='https://github.com/xflr6/bitsets',
    project_urls={
        'Documentation': 'https://bitsets.readthedocs.io',
        'Changelog': 'https://bitsets.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/xflr6/bitsets/issues',
        'CI': 'https://travis-ci.org/xflr6/bitsets',
        'Coverage': 'https://codecov.io/gh/xflr6/bitsets',
    },
    packages=find_packages(),
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    extras_require={
        'dev': ['tox>=3', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=4', 'pytest-cov'],
        'docs': ['sphinx>=1.8', 'sphinx-rtd-theme'],
        'visualization': ['graphviz~=0.7'],
    },
    long_description=io.open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
