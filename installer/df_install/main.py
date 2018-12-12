#!/usr/bin/env python

import sys

from .cmd import base
from .cmd import install_fonts, link_configs, setup_venv


def run():
    base.cli()


if __name__ == '__main__':
    run()
