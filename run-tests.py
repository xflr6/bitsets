#!/usr/bin/env python3

import platform
import sys

import pytest

ARGS = [#'--pdb',
        #'--exitfirst',
        ]

if platform.system() == 'Windows':
    if 'idlelib' in sys.modules:
        ARGS += ['--capture=sys', '--color=no']

sys.exit(pytest.main(ARGS + sys.argv[1:]))
