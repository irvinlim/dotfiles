#!/usr/bin/env python

# pylint: skip-file

import sys

from .cmd import base
from .cmd import install_fonts, link_configs, setup_venv


def run():
    if not base.cli(standalone_mode=False):
        sys.exit(1)


if __name__ == '__main__':
    run()
