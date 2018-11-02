# Cross-compatible shims, no using six here...

try:
    input = raw_input
except NameError:
    pass

try:
    basestring
except NameError:
    basestring = str
