from __future__ import print_function

import click
import yaml

from .base import cli
from df_install.utils import log, merge, process, plist
from df_install.utils.constants import *

TYPEDEFS = {
    'bool': bool,
    'int': int,
    'float': float,
    'string': str,
}


def load_config(filepath):
    configs = []
    with open(filepath, 'r') as f:
        # Load each doc
        docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in docs:
            configs.append(doc)

    return configs


def merge_configs(configs):
    result = {}
    for config in configs:
        merge.dict_merge(result, config)

    return result


def get_write_args(value):
    # Dynamically typed value (using schema)
    if isinstance(value, dict):
        type_name = value.get('type')

        # Handle special types
        if type_name == 'array':
            args = _get_array_write_args(value)
            if args is not None:
                return args

        # Resolve type definition using schema
        if type_name in TYPEDEFS:
            return _get_value_from_typedef(type_name, value.get('value'))

    # Fallback to static type definitions (single value)
    return _get_typed_value(value)


def _get_array_write_args(value):
    operation = value.get('operation')

    # Clear array value
    if operation == 'clear':
        return '-array',

    # Set array value from 'items' field.
    # TODO: Experimental.
    if operation == 'set':
        return "'%s'" % plist.dumps(value.get('items')),

    return None


def _get_typed_value(value):
    for type_name, typedef in TYPEDEFS.items():
        if isinstance(value, typedef):
            return _get_value_from_typedef(type_name, value)

    raise Exception('Unknown type for value: %s' % value)


def _get_value_from_typedef(type_name, value):
    return '-' + type_name, plist.dumps(value)


def generate_cmd(domain, key, *args):
    return 'defaults write %s %s %s' % (domain, key, ' '.join(args))


def apply_config(config):
    commands = []

    # Generate commands for config
    for app_name, meta in config.items():
        app_configs = meta.get('configs')
        for domain, app_config in app_configs.items():
            for key, value in app_config.items():
                # Determine type of value
                args = get_write_args(value)

                # Generate command
                command = generate_cmd(domain, key, *args)
                commands.append(command)

    # Print commands to be executed
    log.debug('[*] Applying defaults:')
    for command in commands:
        log.debug('    %s' % command)

    # Execute commands
    # TODO: Execute commands using exec form like in Dockerfile.
    log.info('[*] Applying defaults...')
    retcode, stdout, stderr = process.execute_cmds(commands, fail_on_error=True)

    if stdout:
        log.info('[!] Command stdout:\n%s' % stdout)

    if retcode != 0:
        log.error('[!] Command stderr:\n%s' % stderr)
        raise Exception('Applying configs returned exit code %d' % retcode)


def restart_apps(config):
    apps = set()
    for _, meta in config.items():
        for app in meta.get('restart', []):
            apps.add(app)

    log.debug('[*] Sending SIGTERM to apps:')
    for app in sorted(apps):
        log.debug('    %s' % app)

    # Simply send SIGTERM to apps which will restart.
    # TODO: Maybe consider adding a restart signal in the config to differentiate.
    log.info('[*] Restarting apps...')
    process.pkill(apps)


@cli.command()
@click.option(
    '--file', '-f', default=MACOS_DEFAULTS_CONFIGS, multiple=True,
    help='Path to YAML file for macOS defaults config.',
)
@click.option('--restart/--no-restart', default=False, help='Whether to restart configured applications.')
def set_macos_defaults(file, restart):
    # Parse all config files
    configs = []
    for config_path in file:
        log.debug('[+] Loading config file: %s' % config_path)
        for config in load_config(config_path):
            configs.append(config)

    # Merge configs
    full_config = merge_configs(configs)

    # Apply configs
    try:
        apply_config(full_config)
    except Exception as e:
        log.error('[!] Exception while applying configs: %s' % str(e))
        return False

    # Restart applications
    if restart:
        restart_apps(full_config)

    log.success('[*] Successfully applied configs.')
    return True


if __name__ == '__main__':
    set_macos_defaults()
