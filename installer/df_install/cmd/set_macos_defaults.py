from __future__ import print_function

import click
import yaml

from .base import cli
from df_install.utils import log, merge, process
from df_install.utils.constants import *


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


def get_typed_value(value):
    if isinstance(value, bool):
        if value is True:
            value = 'true'
        elif value is False:
            value = 'false'
        else:
            raise Exception('Unexpected value for bool: %s' % value)
        return '-bool', value
    if isinstance(value, int):
        return '-int', value
    if isinstance(value, float):
        return '-float', value
    if isinstance(value, str):
        return '-string', value
    raise Exception('Unknown type for value: %s' % value)


def generate_cmd(domain, key, vtype, value):
    return 'defaults write %s %s %s %s' % (domain, key, vtype, value)


def apply_config(config):
    commands = []

    # Generate commands for config
    for app, app_config in config.items():
        domain = app_config.get('domain')
        if not domain:
            log.error('[!] No domain set for %s.' % app)
            continue

        for key, value in app_config.get('configs').items():
            # Determine type of value
            vtype, value = get_typed_value(value)

            # Generate command
            command = generate_cmd(domain, key, vtype, value)
            commands.append(command)

    # Print commands to be executed
    log.info('[*] Applying defaults:\n%s' % '\n'.join(commands))

    # Execute commands
    retcode, stdout, stderr = process.execute_cmds(commands)

    if stdout:
        print(stdout)
    if stderr:
        print(stderr)

    if retcode != 0:
        raise Exception('Commands returned exit code %d' % retcode)


def restart_apps(config):
    apps = set()
    for app in config:
        apps.add(app)

    # Simply send SIGTERM to apps which will restart.
    # TODO: Maybe consider adding a restart signal in the config to differentiate.
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
    restart_apps(full_config)

    log.success('[*] Successfully applied configs.')
    return True


if __name__ == '__main__':
    set_macos_defaults()
