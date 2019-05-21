from __future__ import print_function

import json
import os
import sys

import click
from six import string_types
from virtualenvapi.manage import VirtualEnvironment

from .base import cli
from df_install.utils import log

DOTFILES_ROOT = os.getenv('DOTFILES_ROOT')
GLOBAL_VIRTUALENV_ROOT = os.path.expanduser('~/.virtualenvs')
LOCAL_VIRTUALENV_PATH = '.venv'
VIRTUALENVS_JSON = os.path.join(DOTFILES_ROOT, 'packages', 'virtualenvs.json')


def get_requirements(filenames):
    requirements = []
    for filename in filenames:
        with open(os.path.join(DOTFILES_ROOT, 'packages/virtualenv/%s.txt' % filename)) as f:
            requirements += [line.rstrip('\n') for line in f if line.rstrip('\n') and not line.startswith('#')]

    requirements.sort()
    return requirements


def resolve_python_paths(interpreter, data):
    python_paths = data.get('pythonPaths').get(interpreter, [])

    if isinstance(python_paths, string_types):
        python_paths = [python_paths]

    python_path = None
    for path in python_paths:
        path = os.path.expanduser(path)
        if os.path.exists(path):
            python_path = path
            break

    return python_path


def install_venv(name, path, requirements, python_path):
    print('[*] Setting up %s virtualenv...' % log.color('1;34', name))

    try:
        # Create new virtualenv if it doesn't exist.
        env = VirtualEnvironment(path, python=python_path)

        # Install requirements for the virtualenv.
        requirements = get_requirements(requirements)
        for requirement in requirements:
            requirement = requirement.split(' ')
            package, options = requirement[0], requirement[1:]

            if not env.is_installed(package):
                print('    Installing %s...' % log.color('1;33', package))
                env.install(package, options=options)
    except Exception as e:
        log.error('Exception occurred while setting up %s: %s' % (name, e))


def setup_from(venv_name):
    with open(VIRTUALENVS_JSON) as f:
        data = json.load(f)

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
    install_venv(LOCAL_VIRTUALENV_PATH, LOCAL_VIRTUALENV_PATH, requirements, python_path)
    return True


def setup_venvs_from_config():
    log.info('Installing virtualenvs from config...')

    with open(VIRTUALENVS_JSON) as f:
        data = json.load(f)

    venvs = data.get('venvs')

    for name, venv in venvs.items():
        requirements = venv.get('requirements')
        python_path = resolve_python_paths(venv.get('interpreter'), data)
        if not python_path:
            log.error('Cannot setup virtualenv for %s, no valid interpreter path found.' % name)
            continue

        path = os.path.join(GLOBAL_VIRTUALENV_ROOT, name)
        install_venv(name, path, requirements, python_path)

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


@cli.command()
@click.option('--from', 'venv_name', help='Virtualenv to create from.')
@click.option('--from-config', is_flag=True, help='Whether to setup all virtualenvs from the config file.')
def setup_venv(venv_name, from_config):
    if from_config is True:
        return setup_venvs_from_config()

    if not venv_name:
        log.error('Virtualenv name not specified.')
        return False

    if venv_name == 'base':
        return setup_venv_from_base()

    return setup_venv_from(venv_name)


if __name__ == '__main__':
    if not os.path.exists(GLOBAL_VIRTUALENV_ROOT):
        os.makedirs(GLOBAL_VIRTUALENV_ROOT)

    setup_venv()  # pylint: disable=no-value-for-parameter
