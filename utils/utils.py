import argparse


def dict2namespace(config):
    namespace = argparse.Namespace()
    for k, v in config.items():
        if isinstance(v, dict):
            new_value = dict2namespace(v)
        else:
            new_value = v
        setattr(namespace, k, new_value)
    return namespace


def namespace2dict(name_space):
    if not isinstance(name_space, argparse.Namespace):
        return name_space
    if isinstance(name_space, argparse.Namespace):
        name_space = name_space.__dict__
    adict = dict()
    for key, value in name_space.items():
        adict[key] = namespace2dict(value)
    return adict
