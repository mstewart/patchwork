"""
Fabric utilities for managing Redhat-style RPM packages.
"""

from fabric.api import run, settings, hide
from errors import PackageInstallationError

def is_installed(*packages):
    """
    Checks whether ``packages`` are all installed on the system.
    """
    if not packages:
        return True
    with settings(hide('stdout', 'stderr', 'warnings'), warn_only=True):
        return run("rpm --query --quiet %s" % " ".join(packages)).succeeded


def install(*packages, **kwargs):
    """
    Takes an iterable of strings; ensure all packages with these names are installed.
    Idempotent operation.

    Set ``use_epel=True`` if yum should use the pseudo-standard EPEL repos.

    Note: in some RHEL versions, yum has a bug where it doesn't return an
    error code when trying to install a nonexistent package.
    See e.g.
    * https://bugzilla.redhat.com/show_bug.cgi?id=736694
    * http://tickets.opscode.com/browse/CHEF-2062
    So a followup query check is unfortunately necessary for portability.
    """
    use_epel = kwargs.get('use_epel', False)
    epel_option = "--enablerepo=epel " if use_epel else ""
    package_list = " ".join(packages)
    sudo("yum install --assumeyes %(epel_option)s %(package_list)s" % locals())
    if not is_installed(*packages):
        raise PackageInstallationError("yum reported success in installing " +
                "the following packages, but they are not all present: " +
                ",".join(packages))

