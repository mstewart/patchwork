from fabric.api import *

def exists(name):
    """
    Check if user exists
    """
    with settings(hide('stdout', 'warnings'), warn_only=True):
        return run('getent passwd %(name)s' % locals()).succeeded


def create(name, home=None, shell=None, uid=None, gid=None, groups=None):
    """
    Create a new user
    """
    options = []
    if gid:
        options.append('--gid "%s"' % gid)
    if groups:
        if not isinstance(groups, basestring):
            groups = ','.join('"%s"' % group for group in groups)
        options.append('--groups %s' % groups)
    if home:
        options.append('--home "%s"' % home)
    if shell:
        options.append('--shell "%s"' % (shell))
    if uid:
        options.append('--uid %s' % uid)
    options = " ".join(options)
    sudo('useradd %(options)s %(name)s' % locals())

def get_homedir(user):
    """
    Use python on the remote end to avoid reinventing the wheel by
    having yet another passwd entry parser.
    """
    return run("python -c 'import pwd; print(pwd.getpwnam(%s).pw_dir)'").stdout

def add_to_group(username, groupname):
    """
    Add a user to a group.  Idempotent operation.
    """
    sudo('usermod -G "%s" --append "%s"' % (groupname, username))
