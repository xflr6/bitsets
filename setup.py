# setup.py

from setuptools import setup, find_packages

setup(
    name='bitsets',
    version='0.7.7',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Ordered subsets over a predefined domain',
    keywords='ordered set finite immutable bit string array map field',
    license='MIT',
    url='http://github.com/xflr6/bitsets',
    packages=find_packages(),
    extras_require={
        'visualization': ['graphviz>=0.3, <0.4'],
        'dev': ['wheel'],
        'test': ['nose', 'coverage', 'flake8', 'pep8-naming'],
    },
    platforms='any',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
