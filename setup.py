# setup.py

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='bitsets',
    version='0.6.1',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Ordered subsets over a predefined domain',
    keywords='ordered set finite immutable bit string array map field',
    license='MIT',
    url='http://github.com/xflr6/bitsets',
    packages=['bitsets'],
    platforms='any',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
