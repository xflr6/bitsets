#!/usr/bin/env python3

"""Run the tests with https://pytest.org."""

import pathlib
import platform
import sys

import pytest

SELF = pathlib.Path(__file__)

ARGS = [#'--pdb',
        #'--exitfirst',
        ]

if platform.system() == 'Windows' and 'idlelib' in sys.modules:
    ARGS += ['--capture=sys', '--color=no']


print('run', [SELF.name] + sys.argv[1:])
args = ARGS + sys.argv[1:]

print(f'pytest.main({args!r})')
sys.exit(pytest.main(args))
