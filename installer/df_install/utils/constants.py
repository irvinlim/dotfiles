import os

DOTFILES_ROOT = os.getenv('DOTFILES_ROOT')
GLOBAL_VIRTUALENV_ROOT = os.path.expanduser('~/.virtualenvs')
LOCAL_VIRTUALENV_PATH = '.venv'
VIRTUALENVS_JSON = os.path.join(DOTFILES_ROOT, 'packages', 'virtualenvs.json')
