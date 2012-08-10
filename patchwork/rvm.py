from fabric.api import run, sudo, settings, hide, env
from fabric.context_managers import prefix

import files, users

DEFAULT_RUBY_VERSION='1.9.2'

def system_installation(rvm_users=None):
    """
    Install system-wide RVM.

    The specified ``rvm_users`` will be added to the ``rvm`` user group.
    If none are specified, the runas user only will be added.

    This always installs the latest version, which is bad: installs at different times
    get different RVM versions.
    TODO: Freeze it at one git hash.
    """
    if rvm_users is None:
        rvm_users = [env.user]

    if not files.exists('/usr/local/rvm'):
        run('curl -L https://get.rvm.io | sudo TERM=dumb bash -s stable', shell=True, pty=True)
    for rvm_user in rvm_users:
        users.add_to_group(user=rvm_user, group='rvm')

def gemset(gemsetname, ruby_version=DEFAULT_RUBY_VERSION):
    """
    Ensure an rvm with this gemset exists, and return a context manager
    for executing commands in this gemset.

    E.g.
        with rvm.gemset('production', ruby_version='1.9.2'):
            run('bundle install foolib')
    """
    # Install the interpreter of this version
    run('rvm install %(ruby_version)s' % locals())

    rvm_use_cmd = 'rvm use %(ruby_version)s@%(gemsetname)s' % locals()
    run(rvm_use_cmd + ' --create')
    return prefix(rvm_use_cmd)
