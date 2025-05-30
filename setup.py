import pathlib
from setuptools import setup, find_packages

setup(
    name='bitsets',
    version='0.8.5.dev0',
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
        'CI': 'https://github.com/xflr6/bitsets/actions',
        'Coverage': 'https://codecov.io/gh/xflr6/bitsets',
    },
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.9',
    extras_require={
        'dev': ['tox>=3', 'flake8', 'pep8-naming', 'wheel', 'twine'],
        'test': ['pytest>=7', 'pytest-cov'],
        'docs': ['sphinx>=5', 'sphinx-rtd-theme'],
        'visualization': ['graphviz~=0.7'],
    },
    long_description=pathlib.Path('README.rst').read_text(encoding='utf-8'),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)
