from fabric.api import sudo
from patchwork.info import distro_family
from errors import UnsupportedDistributionError

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
        raise UnsupportedDistributionError('System type detected as "' + family +
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


def multi_distro_install(distro_to_package_map):
    """
    Utility function for installing different packages, depending on the
    distro we're on.

    This will install the list of packages
        ``distro_to_package_map[distro_family()]``
    or else raise an UnsupportedDistributionError if there are no packages
    mapped to that distro family.
    """
    distro_family = info.get_distro_family()
    try:
        packages.install(distro_to_package_map[info.get_distro_family()])
    except KeyError:
        raise packages.UnsupportedDistributionError("Operation not supported" +
                " for distro family %s" % distro_family)

def rubygem(gem):
    """
    Install a Rubygem
    """
    return sudo("gem install -b --no-rdoc --no-ri %s" % gem)
