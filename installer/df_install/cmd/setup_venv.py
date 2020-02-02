from __future__ import print_function

import json
import os
import shutil
import sys
import traceback

from virtualenvapi.exceptions import VirtualenvCreationException
from virtualenvapi.manage import VirtualEnvironment

import click
from df_install.cmd.base import cli
from df_install.utils import log, virtualenvs
from df_install.utils.constants import *


def get_requirements(filenames):
    requirements = []
    for filename in filenames:
        with open(os.path.join(DOTFILES_ROOT, 'packages/virtualenv/%s.txt' % filename)) as f:
            requirements += [line.rstrip('\n') for line in f if line.rstrip('\n') and not line.startswith('#')]

    requirements.sort()
    return requirements


def install_venv(name, path, requirements, python_path):
    print('[*] Setting up %s virtualenv...' % log.color('1;34', name))

    try:
        # Create new virtualenv if it doesn't exist.
        if not os.path.exists(path):
            env = VirtualEnvironment(path, python=python_path)
            env.open_or_create()

        # Reopen virtualenv to use the correct Python path
        env = VirtualEnvironment(path)
        assert env.path == os.path.abspath(path)

        # Install requirements for the virtualenv.
        # TODO: Shebang lines in binaries installed this way
        #       use the path in python_path instead of this virtualenv's,
        #       which I haven't been able to solve yet. A workaround
        #       is just to pip uninstall and then install it back.
        requirements = get_requirements(requirements)
        for requirement in requirements:
            requirement = requirement.split(' ')
            package, options = requirement[0], requirement[1:]

            if not env.is_installed(package):
                print('    Installing %s...' % log.color('1;33', package))
                env.install(package, options=options)
    except AssertionError as e:
        raise e
    except VirtualenvCreationException as e:
        # Could not create virtualenv, which executes `virtualenv` as a subprocess under the hood.
        log.error('Exception occurred while creating virtualenv: %s' % e)

        # Check if we can find the virtualenv bin.
        which = shutil.which('virtualenv')
        if which is None:
            log.error('Most probable error: Could not locate `virtualenv` in $PATH.')
            return False

        log.error('Possible errors:\n' + \
                  '1. Check the shebang of %s' % which)

        return False
    except Exception as e:
        log.error('Exception (%s) occurred while setting up %s: %s' % (e.__class__, name, e))
        traceback.print_exc()
        return False

    return True


def setup_from(venv_name):
    data = virtualenvs.get_virtualenvs()
    venv_from = data.get('venvs').get(venv_name)
    if not venv_from:
        log.error('No virtualenv config named "%s" found.' % venv_name)
        return False

    requirements = venv_from.get('requirements')
    python_path = resolve_python_paths(venv_from.get('interpreter'), data)
    if not python_path:
        log.error('No valid interpreter path found.')
        return False

    log.debug('Using Python interpreter %s.' % python_path)
    return install_venv(LOCAL_VIRTUALENV_PATH, LOCAL_VIRTUALENV_PATH, requirements, python_path)


def setup_venvs_from_config():
    log.info('Installing virtualenvs from config...')

    data = virtualenvs.get_virtualenvs()
    venvs = data.get('venvs')

    for name, venv in venvs.items():
        requirements = venv.get('requirements')
        python_path = resolve_python_paths(venv.get('interpreter'), data)
        if not python_path:
            log.error('Cannot setup virtualenv for %s, no valid interpreter path found.' % name)
            continue

        path = os.path.join(GLOBAL_VIRTUALENV_ROOT, name)
        if not install_venv(name, path, requirements, python_path):
            return False

    log.success('All virtualenvs have been set up!')
    return True


def setup_venv_from(venv_name):
    if not venv_name:
        log.error('Please specify venv name.')
        return False

    log.info('Installing virtualenv from %s...' % venv_name)

    if not setup_from(venv_name):
        return False


def setup_venv_from_base():
    if os.path.exists(os.path.abspath(LOCAL_VIRTUALENV_PATH)):
        log.error('Virtualenv already exists.')
        return False

    if not setup_from('base'):
        return False

    print(log.color('0;32', 'Virtualenv is created! Now run'), log.color('1;34', 'venv'), log.color('0;32', 'in your shell to activate.'))
    return True


def setup_venv_from_python_path(python_path):
    if os.path.exists(os.path.abspath(LOCAL_VIRTUALENV_PATH)):
        log.error('Virtualenv already exists.')
        return False

    log.debug('Using Python interpreter %s.' % python_path)

    # Install new Virtualenv locally
    if not install_venv(LOCAL_VIRTUALENV_PATH, LOCAL_VIRTUALENV_PATH, [], python_path):
        return False

    print(log.color('0;32', 'Virtualenv is created! Now run'), log.color('1;34', 'venv'), log.color('0;32', 'in your shell to activate.'))
    return True


@cli.command()
@click.argument(
    'venv_name',
    required=False,
)
@click.option(
    '--from-config',
    is_flag=True,
    help='Whether to setup all virtualenvs from the config file.',
)
@click.option(
    '--python-path',
    help='Path to specific Python interpreter.',
)
def setup_venv(venv_name, from_config, python_path):
    if from_config is True:
        return setup_venvs_from_config()

    if python_path:
        return setup_venv_from_python_path(python_path)

    if not venv_name:
        return setup_venv_from_base()

    return setup_venv_from(venv_name)


if __name__ == '__main__':
    if not os.path.exists(GLOBAL_VIRTUALENV_ROOT):
        os.makedirs(GLOBAL_VIRTUALENV_ROOT)

    setup_venv()  # pylint: disable=no-value-for-parameter
