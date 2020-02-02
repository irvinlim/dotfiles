"""
Attempts to fix virtualenvs after a Homebrew Python upgrade.
This is inspired from the blog post at
http://www.jeremycade.com/python/osx/homebrew/2015/03/02/fixing-virtualenv-after-a-python-upgrade/.
"""

import os

import click
from six.moves import input
from virtualenvapi.manage import VirtualEnvironment

from df_install.cmd.base import cli
from df_install.utils import log, virtualenvs
from df_install.utils.constants import LOCAL_VIRTUALENV_PATH


@cli.command()
@click.argument('path', required=False)
@click.option('--python', help='Name of Python interpreter to recreate the virtualenv with.')
@click.option('--python-path', help='Path to Python interpreter to recreate the virtualenv with.')
@click.option('--force', '-f', is_flag=True, help='Force remove all symlinks in the virtualenv. This might break more things!')
def fix_venv(path, python, python_path, force):
    # Default to local venv path in current directory
    if not path:
        path = LOCAL_VIRTUALENV_PATH

    path = os.path.abspath(path)

    # Make sure virtualenv path exists
    if not os.path.exists(path):
        log.error('Virtualenv path does not exist: %s' % path)
        return False

    # Validate either Python interpreter or Python path
    if not python and not python_path:
        log.error(
            'Please specify either a Python interpreter (with --python) or Python path (with --python-path) to recreate the virtualenv with.'
        )
        return False

    if python:
        data = virtualenvs.get_virtualenvs()
        python_path = virtualenvs.resolve_python_paths(python, data)
        if not python_path:
            log.error('No valid interpreter path found for %s.' % python)
            log.info('Valid interpreters: %s' % ', '.join(data.get('pythonPaths').keys()))
            return False

    # Confirmation prompt
    yes = input('Are you sure you want to fix the virtualenv at %s? [y/n] ' % path).upper() == 'Y'
    if not yes:
        log.info('Aborting.')
        return False

    # Remove all symlinks in the virtualenv
    log.info('Removing broken symlinks in virtualenv...')
    num_broken = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)

            # Find broken symlinks, or any symlink if -f is passed
            if os.path.islink(fullpath) and (force or not os.path.exists(fullpath)):
                log.debug('Removing symlink %s' % fullpath)
                os.unlink(fullpath)
                num_broken += 1

    if num_broken == 0:
        log.error('No broken symlinks found. Aborting.')
        return False

    # Recreate virtualenv
    log.info('Recreating virtualenv using %s...' % python_path)
    env = VirtualEnvironment(path, python=python_path)
    env._create()

    log.success('Done!')
