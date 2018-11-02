# Cross-compatible shims, no using six here...

try:
    input_function = raw_input
except NameError:
    input_function = input

try:
    basestring
except NameError:
    basestring = str
