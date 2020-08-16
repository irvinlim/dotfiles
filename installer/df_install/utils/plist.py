def dumps(value):
    if isinstance(value, list):
        return '(%s)' % ','.join(dumps(item) for item in value)
    if isinstance(value, dict):
        return '{%s}' % '; '.join('%s = %s' % (key, dumps(value)) for key, value in value.items())

    if isinstance(value, bool):
        if value is True:
            return 'true'
        elif value is False:
            return 'false'
        else:
            raise Exception('Invalid boolean: %s' % value)

    if isinstance(value, int):
        return '%s' % value
    if isinstance(value, float):
        return '%s' % value
    if isinstance(value, str):
        return '%s' % value
