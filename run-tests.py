#!/usr/bin/env python3

"""Run the tests with https://pytest.org."""

import platform
import sys

import pytest

ARGS = [#'--pdb',
        #'--exitfirst',
        ]

if platform.system() == 'Windows' and 'idlelib' in sys.modules:
    ARGS += ['--capture=sys', '--color=no']

sys.exit(pytest.main(ARGS + sys.argv[1:]))
