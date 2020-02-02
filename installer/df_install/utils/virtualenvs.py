import json
import os

from six import string_types

from .constants import VIRTUALENVS_JSON


def get_virtualenvs():
    with open(VIRTUALENVS_JSON) as f:
        return json.load(f)


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
