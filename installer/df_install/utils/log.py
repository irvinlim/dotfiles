from __future__ import print_function


def success(*msg, **kwargs):
    sep = kwargs.pop('sep', ' ')
    print(color('0;32', *msg, sep=sep), **kwargs)


def info(*msg, **kwargs):
    sep = kwargs.pop('sep', ' ')
    print(color('0;33', *msg, sep=sep), **kwargs)


def error(*msg, **kwargs):
    sep = kwargs.pop('sep', ' ')
    print(color('0;31', *msg, sep=sep), **kwargs)


def debug(*msg, **kwargs):
    sep = kwargs.pop('sep', ' ')
    print(color('0;36', *msg, sep=sep), **kwargs)


def color(colorcode, *msg, **kwargs):
    sep = kwargs.pop('sep', ' ')
    return '\033[%sm' % colorcode + sep.join(msg) + '\033[0m'
