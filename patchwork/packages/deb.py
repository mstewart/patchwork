from fabric.api import run, sudo, settings, hide

def is_installed(packages):
    """
    Check whether ``packages`` are all installed on the system
    using ``dpkg-query``.
    """
    if not packages:
        return True
    if isinstance(packages, basestring):
        packages = [packages]
    with settings(hide('stdout', 'stderr', 'warnings'), warn_only=True):
        return run('dpkg-query --show %s' % " ".join(packages)).succeeded

def install(packages, **kwargs):
    """
    Ensure all ``packages`` are installed with ``apt-get``.
    Idempotent operation.
    """
    if not packages:
        return
    if isinstance(packages, basestring):
        packages = [packages]
    # Try to suppress interactive prompts, assume 'yes' to all questions
    sudo('DEBIAN_FRONTEND=noninteractive apt-get install --assume-yes --quiet %s' % " ".join(packages))
