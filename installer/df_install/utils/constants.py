import os

DOTFILES_ROOT = os.getenv('DOTFILES_ROOT')
GLOBAL_VIRTUALENV_ROOT = os.path.expanduser('~/.virtualenvs')
LOCAL_VIRTUALENV_PATH = '.venv'
VIRTUALENVS_JSON = os.path.join(DOTFILES_ROOT, 'packages', 'virtualenvs.json')

CONFIGS_ROOT = os.path.join(DOTFILES_ROOT, 'configs')
MACOS_DEFAULTS_CONFIGS = [
    os.path.join(CONFIGS_ROOT, 'macos', 'defaults.yml'),
]
