import redhat, debian

from patchwork.info import distro_family

def _implementor():
    """
    Return the module implementing mysql operations for the
    current distro.
    """
    mappings = {
            'redhat': redhat,
            'debian': debian
            }
    family = distro_family()
    try:
        return mappings[family]
    except KeyError:
        raise UnsupportedDistributionError('System type detected as "' + family +
                '"; mysql management not implemented for this type.')


def client():
    return _implementor().client()


def server():
    return _implementor().server()
