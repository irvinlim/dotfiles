#!/usr/bin/env python

# pylint: skip-file

import sys

from .cmd import base
from .cmd import fix_venv, install_fonts, link_configs, set_macos_defaults, setup_venv, version


def run():
    if not base.cli(standalone_mode=False):
        sys.exit(1)


if __name__ == '__main__':
    run()
