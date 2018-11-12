from __future__ import print_function


def success(*msg, sep=' ', **kwargs):
    print(color('0;32', *msg, sep=sep), **kwargs)


def info(*msg, sep=' ', **kwargs):
    print(color('0;33', *msg, sep=sep), **kwargs)


def error(*msg, sep=' ', **kwargs):
    print(color('0;31', *msg, sep=sep), **kwargs)


def color(colorcode, *msg, sep=' '):
    return '\033[%sm' % colorcode + sep.join(msg) + '\033[0m'
