#!/usr/bin/env python

from __future__ import print_function

import json
import os
import shutil
from sys import platform

# Cross-compatible shims, no using six here...
try:
    input = raw_input
except NameError:
    pass

try:
    basestring
except NameError:
    basestring = str


def get_dst(src, dst):
    if isinstance(dst, basestring):
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
        raise Exception('Mapping for %s is not provided for %s, cannot fallback on `linux`.' % (platform, src))
    return linux


def link_file(src, dst):
    # Skip if symlink is identical.
    if os.path.islink(dst) and os.readlink(dst) == src:
        return

    print('[*] Linking %s to %s...' % (os.path.basename(src), dst))

    # Prompt before overwriting file.
    write = True
    if os.path.exists(dst) or os.path.islink(dst):
        write = input('[?] %s exists. Overwrite? (y/N) ' % dst).upper() == 'Y'
        if not write:
            return

        if os.path.isfile(dst):
            os.unlink(dst)
        else:
            shutil.rmtree(dst)

    dirname = os.path.dirname(dst)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    os.symlink(src, dst)


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
    print('\033[0;33mLinking configuration files...\033[0m')

    with open('file_mapping.json') as f:
        for src, dst in json.load(f).items():
            src_path = os.path.abspath(os.path.join(src))
            dst_path = os.path.abspath(os.path.expanduser(os.path.join(get_dst(src, dst))))
            iterate_directory(src_path, dst_path)

    with open('dir_mapping.json') as f:
        for mapping in json.load(f):
            src = mapping.get('src')
            dst = mapping.get('dst')
            src_path = os.path.abspath(os.path.join(src))
            dst_path = os.path.abspath(os.path.expanduser(os.path.join(get_dst(src, dst))))
            link_file(src_path, dst_path)

    print('\033[0;32mAll configuration files linked!\033[0m')


if __name__ == '__main__':
    main()
