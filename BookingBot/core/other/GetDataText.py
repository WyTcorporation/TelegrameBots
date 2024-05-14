def dictLine(dicts):
    result = []

    def listDict(d):
        for k, v in d.items():
            if isinstance(v, dict):
                listDict(v)
            else:
                result.append(f'{k.capitalize()}: {v}')

    listDict(dicts)
    return ';\r\n'.join(result)
