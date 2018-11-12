#!/usr/bin/env python

from __future__ import print_function

import json
import os
import sys

from virtualenvapi.manage import VirtualEnvironment

from . import log
from .utils import basestring_type

DOTFILES_ROOT = os.getenv('DOTFILES_ROOT') or os.path.abspath(os.path.curdir)
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


def resolve_python_paths(python_paths):
    if isinstance(python_paths, basestring_type):
        python_paths = [python_paths]

    python_path = None
    for path in python_paths:
        if os.path.exists(path):
            python_path = path
            break

    return python_path


def install_venv(name, path, requirements, python_path):
    print('[*] Setting up %s virtualenv...' % log.color('1;34', name))

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


def setup_venvs_from_config():
    log.info('Installing virtualenvs from config...')

    with open(VIRTUALENVS_JSON) as f:
        data = json.load(f)

    venvs = data.get('venvs')
    from_paths = data.get('fromPaths')

    for name, venv in venvs.items():
        requirements = venv.get('requirements')
        python_path = resolve_python_paths(from_paths.get(venv.get('from')))
        if not python_path:
            log.error('[!] Cannot setup virtualenv for %s, no valid fromPath found.')
            continue

        path = os.path.join(GLOBAL_VIRTUALENV_ROOT, name)
        install_venv(name, path, requirements, python_path)

    log.success('All virtualenvs have been set up!')


def setup_venv_from(venv_name=""):
    if not venv_name:
        log.error('Please specify venv name.')
        sys.exit(-1)

    log.info('Installing virtualenv from %s...' % venv_name)

    with open(VIRTUALENVS_JSON) as f:
        data = json.load(f)

    venv_from = data.get('venvs').get(venv_name)
    if not venv_from:
        log.error('No virtualenv config named "%s" found.' % venv_name)
        sys.exit(-1)

    requirements = venv_from.get('requirements')
    python_path = resolve_python_paths(data.get('fromPaths').get(venv_from.get('from')))

    log.debug('Using Python interpreter %s.' % python_path)
    install_venv(LOCAL_VIRTUALENV_PATH, LOCAL_VIRTUALENV_PATH, requirements, python_path)


def setup_venv_from_base():
    if os.path.exists(os.path.abspath(LOCAL_VIRTUALENV_PATH)):
        log.error('Virtualenv already exists.')
        sys.exit(-1)

    setup_venv_from('base')

    print(log.color('0;32', 'Virtualenv is created! Now run'), log.color('1;34', 'venv'), log.color('0;32', 'in your shell to activate.'))


def main():
    commands = {
        'from': setup_venv_from,
        'from_config': setup_venvs_from_config,
        'from_base': setup_venv_from_base,
    }
    command_keys = list(commands.keys())

    if len(sys.argv) < 2:
        print('Usage: python setup_venv.py [%s]' % '|'.join(command_keys))
        sys.exit(-1)

    cmd = sys.argv[1]
    if cmd not in commands:
        print('Usage: python setup_venv.py [%s]' % '|'.join(command_keys))
        sys.exit(-1)

    commands[cmd](*sys.argv[2:])


if __name__ == '__main__':
    main()
