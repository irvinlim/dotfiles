import os
from contextlib import contextmanager

from setuptools import find_packages, setup

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


@contextmanager
def cd(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


def _setup():
    with cd(PROJECT_DIR):
        install_requires = []
        for requirement in open(os.path.join('requirements.txt')).readlines():
            requirement = requirement.strip()
            if requirement and requirement[0] != '#':
                install_requires.append(requirement)

        setup(
            name='df-install',
            version='1.1.0',
            author='Irvin Lim',
            author_email='me@irvinlim.com',
            url='https://github.com/irvinlim/dotfiles',
            install_requires=install_requires,
            packages=find_packages(),
            entry_points={'console_scripts': ['df-install = df_install.main:run']},
        )


if __name__ == '__main__':
    _setup()
