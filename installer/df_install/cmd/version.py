from __future__ import print_function

import pkg_resources

from .base import cli

@cli.command()
def version():
    print(pkg_resources.get_distribution('df-install').version)
