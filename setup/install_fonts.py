#!/usr/bin/env python

from __future__ import print_function

import os
import sys

import requests
from six.moves import urllib

from . import log

fonts = ['https://github.com/powerline/fonts/raw/master/Meslo%20Slashed/Meslo%20LG%20M%20Regular%20for%20Powerline.ttf']

font_locations = {'darwin': '~/Library/Fonts'}


def main():
    font_location = font_locations[sys.platform]

    if not font_location:
        log.error('No font location defined for %s' % sys.platform)
        sys.exit(1)

    for font in fonts:
        font_name = urllib.parse.unquote(os.path.basename(font))
        font_path = os.path.expanduser(os.path.join(font_location, font_name))

        if not os.path.exists(font_path):
            print('[*] Downloading %s...' % log.color('1;33', font_name))

            res = requests.get(font, stream=True)
            if res.status_code != 200:
                log.error('Got status code %s for %s' % (res.status_code, font))
                continue

            with open(font_path, 'wb') as f:
                for chunk in res.iter_content(1024):
                    f.write(chunk)


if __name__ == '__main__':
    main()
