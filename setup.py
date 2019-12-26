# setup.py

import io
from setuptools import setup, find_packages

setup(
    name='bitsets',
    version='0.7.16',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Ordered subsets over a predefined domain',
    keywords='ordered set finite immutable bit string array map field',
    license='MIT',
    url='https://github.com/xflr6/bitsets',
    packages=find_packages(),
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    extras_require={
        'dev': ['flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=3.4,!=3.10.0', 'pytest-cov'],
        'docs': ['sphinx>=1.7', 'sphinx-rtd-theme'],
        'visualization': ['graphviz~=0.7'],
    },
    long_description=io.open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
