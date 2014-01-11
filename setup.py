# setup.py

from distutils.core import setup

setup(
    name='bitsets',
    version='0.1.2',
    url='http://pypi.python.org/pypi/bitsets',
    license='MIT',
    author='Sebastian Bank',
    author_email='sebastian.bank@uni-leipzig.de',
    description='Ordered subsets over a predefined domain',
    long_description=open('README.txt').read(),
    packages=['bitsets'],
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
