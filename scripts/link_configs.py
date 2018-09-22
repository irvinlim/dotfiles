#!/usr/bin/env python

from __future__ import print_function

import json
import os
from sys import platform

# Cross-compatible shims, no using six here...
try:
    input = raw_input
except NameError:
    pass


def get_dst(src, dst):
    if isinstance(dst, str):
        return dst

    linux = dst.get('linux')
    darwin = dst.get('darwin')
    win32 = dst.get('win32')

    # Defaults to Linux if provided platform is not provided.
    # If linux is not provided,
    if platform == 'darwin' and darwin:
        return darwin
    if platform == 'win32' and win32:
        return win32

    if not linux:
        raise Exception(
            'Mapping for %s is not provided for %s, cannot fallback on `linux`.'
            % (platform, src))
    return linux


def link_file(src, dst):
    # Skip if symlink is identical.
    if os.path.islink(dst) and os.readlink(dst) == src:
        return

    print('[*] Linking %s to %s...' % (os.path.basename(src), dst))

    # Prompt before overwriting file.
    write = True
    if os.path.exists(dst):
        write = input('[?] %s exists. Overwrite? (y/N) ' % dst).upper() == 'Y'

    dirname = os.path.dirname(dst)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if write:
        os.symlink(src, dst, False)


def iterate_directory(src, dst):
    for child in os.listdir(src):
        src_path = os.path.join(src, child)
        dst_path = os.path.join(dst, child)

        if not os.path.exists(src_path):
            raise Exception('Error: %s does not exist.' % src_path)

        if os.path.isdir(src_path):
            iterate_directory(src_path, dst_path)
        else:
            link_file(src_path, dst_path)


def main():
    with open('dotfile_mapping.json') as f:
        for src, dst in json.load(f).items():
            src_path = os.path.join(src)
            dst_path = os.path.expanduser(os.path.join(get_dst(src, dst)))
            iterate_directory(src_path, dst_path)


if __name__ == '__main__':
    main()
