from fabric.api import sudo
from patchwork.info import distro_family

import rpm, deb

def _implementor():
    """
    Return the module implementing package management operations for the
    current distro.
    (e.g. the ``rpm`` module for redhat, ``deb`` module for debian).
    """
    mappings = {
            'redhat': rpm,
            'debian': deb
            }
    family = distro_family()
    try:
        return mappings[family]
    except KeyError:
        raise NotImplementedError('System type detected as "' + family +
                '"; package management not implemented for this type.')


def is_installed(*packages):
    """
    Check whether ``packages`` are all installed on the system.
    """
    _implementor().is_installed(*packages)


def install(*packages, **kwargs):
    """
    Ensure all ``packages`` are installed with the system package manager.
    Idempotent operation.
    """
    _implementor().install(*packages, **kwargs)


def package(*packages):
    """
    Ensure all ``packages`` are installed with the system package manager.

    Alias for ``install``.
    """
    install(*packages)


def rubygem(gem):
    """
    Install a Rubygem
    """
    return sudo("gem install -b --no-rdoc --no-ri %s" % gem)
