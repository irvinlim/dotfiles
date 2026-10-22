from __future__ import print_function

try:
    from importlib.metadata import version as get_version
except ImportError:  # Python < 3.8
    from importlib_metadata import version as get_version

from .base import cli

@cli.command()
def version():
    print(get_version('df-install'))
