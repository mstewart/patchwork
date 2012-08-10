from fabric.api import *

class UserCreationError(Exception):
    def __init__(self, msg):
        super(UserCreationError, self).__init__(msg)

class UserDoesNotExistError(Exception):
    def __init__(self, msg):
        super(UserDoesNotExistError, self).__init__(msg)

def exists(name):
    """
    Check if a user with this name exists.
    """
    with settings(hide('stdout', 'warnings'), warn_only=True):
        return run('getent passwd %(name)s' % locals()).succeeded


def create(name, home=None, shell=None, gid=None, groups=None, system=False):
    """
    Create a new user account.

    ``home``: The user's home directory.
        Will not be created if it does not already exist.
    ``shell``: User's login shell.
    ``gid``: Name of the user's primary group.  This group must already exist.
        If not set, a group will be created for the user, with the same
        name as the user.
    ``groups``: The supplemental groups which the user should belong to.
        These must all already exist.
        This can be set to either a single string, where it is interpreted
        as the name of a group; or else an iterable of group names.
    ``system``: Set this flag to create a system account, whose uid (and
        user group gid) is assigned from the system account range instead
        of the user one.
    """
    options = []
    if home:
        options.append('--home "%s"' % home)
    if shell:
        options.append('--shell "%s"' % home)
    if groups:
        if not isinstance(groups, basestring):
            groups = ','.join(groups)
        options.append('--groups %s' % groups)
    if system:
        options.append('--system')

    if gid:
        options.append('--gid "%s"' % gid)
    else:
        options.append('--user-group')

    options = " ".join(options)

    sudo('useradd %(options)s %(name)s' % locals())

def get_homedir(user):
    """
    Return the home directory path for a user.
    Raises an error if the user doesn't exist.

    Use python on the remote end to avoid reinventing the wheel by
    having yet another passwd entry parser.
    """
    if not exists(user):
        raise UserDoesNotExistError('get_homedir: User %s does not exist' % user)
    return run("""python -c 'import pwd; print(pwd.getpwnam("%s").pw_dir)'""" % user).stdout

def add_to_group(user, group):
    """
    Add a user to a group.  Idempotent operation.
    """
    sudo('usermod -G "%s" --append "%s"' % (group, user))
