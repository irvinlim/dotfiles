#!/usr/bin/env python

from __future__ import print_function

import json
import os
import sys

from virtualenvapi.manage import VirtualEnvironment

GLOBAL_VIRTUALENV_ROOT = os.path.expanduser('~/.virtualenvs')
LOCAL_VIRTUALENV_PATH = '.venv'


def get_requirements(filenames):
    requirements = []
    for filename in filenames:
        with open('virtualenv/requirements/%s.txt' % filename) as f:
            requirements += [line.rstrip('\n') for line in f if line.rstrip('\n')]

    requirements.sort()
    return requirements


def install_venv(name, path, requirements, python_path):
    print('[*] Setting up \033[1;34m%s\033[0m virtualenv...' % name)

    # Create new virtualenv if it doesn't exist.
    env = VirtualEnvironment(path, python=python_path)

    # Install requirements for the virtualenv.
    requirements = get_requirements(requirements)
    for requirement in requirements:
        if not env.is_installed(requirement):
            print('    Installing \033[1;33m%s\033[0m...' % requirement)
            env.install(requirement)


def setup_venvs_from_config():
    print('\033[0;33mInstalling virtualenvs from config...\033[0m')

    with open('virtualenvs.json') as f:
        data = json.load(f)

        venvs = data.get('venvs')
        from_paths = data.get('fromPaths')

        for name, venv in venvs.items():
            requirements = venv.get('requirements')
            python_path = from_paths.get(venv.get('from'))
            path = os.path.join(GLOBAL_VIRTUALENV_ROOT, name)
            install_venv(name, path, requirements, python_path)

    print('\033[0;32mAll virtualenvs have been set up!\033[0m')


def setup_venv_from_base():
    with open('virtualenvs.json') as f:
        data = json.load(f)

        base = data.get('base')
        requirements = base.get('requirements')
        python_path = data.get('fromPaths').get(base.get('from'))

        if os.path.exists(os.path.abspath(LOCAL_VIRTUALENV_PATH)):
            print('\033[0;31mVirtualenv already exists.\033[0m')
            sys.exit(-1)

        print('\033[0;33mCreating new virtualenv from %s...\033[0m' % base.get('from'))
        install_venv(LOCAL_VIRTUALENV_PATH, LOCAL_VIRTUALENV_PATH, requirements, python_path)

    print('\033[0;32mVirtualenv is created! Now run \033[1;34mvenv\033[0;32m in your shell to activate.\033[0m')


def main():
    commands = {
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

    commands[cmd]()


if __name__ == '__main__':
    main()
