def flatten_dict(dictionary: dict, separator: str = '/',
                 parent_key: str = '') -> dict:
    flattened = {}
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, dict):
            flattened.update(
                flatten_dict(value, separator=separator, parent_key=new_key))
        else:
            flattened[new_key] = value
    return flattened


def unflatten_dict(dictionary: dict, separator: str = '/') -> dict:
    nested = {}
    for key, value in dictionary.items():
        root = nested
        *parts, k = key.split(separator)
        for part in parts:
            root.setdefault(part, {})
            root = root[part]
        root[k] = value
    return nested
