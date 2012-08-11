from fabric.api import run, sudo, settings, hide, env
from fabric.context_managers import prefix

import files, users, info, require, packages
from packages.errors import PackageInstallationError

# Not actually dependencies for rvm itself, but dependencies of the ruby
# interpreter which rvm needs to build.
RVM_RPM_DEPENDENCIES='gcc-c++ patch readline readline-devel zlib zlib-devel libyaml-devel libffi-devel openssl-devel make bzip2 autoconf automake libtool bison'.split()
RVM_DEB_DEPENDENCIES=[] # Find out what these are

DEFAULT_RUBY_VERSION='1.9.2'

def _install_ruby_system_dependencies():
    if info.distro_family() == 'redhat':
        packages.rpm.install(*RVM_RPM_DEPENDENCIES)
        try:
            # iconv-devel does not exist on some systems, but its contents
            # are usually lumped in with other packages, so this is not
            # generally an error.
            packages.rpm.install('iconv-devel')
        except PackageInstallationError:
            pass

def system_installation(rvm_users=None):
    """
    Install system-wide RVM.

    The specified ``rvm_users`` will be added to the ``rvm`` user group.
    If none are specified, the runas user only will be added.

    This always installs the latest version, which is bad: installs at different times
    get different RVM versions.
    TODO: Add an argument for the version/git hash of RVM to use,
    to allow freezing it.
    """
    if rvm_users is None:
        rvm_users = [env.user]

    if not files.exists('/usr/local/rvm'):
        run('curl -L https://get.rvm.io | sudo TERM=dumb bash -s stable')
    for rvm_user in rvm_users:
        users.add_to_group(user=rvm_user, group='rvm')

def interpreter(ruby_version):
    """Install this version of the ruby interpreter with rvm"""
    _install_ruby_system_dependencies()
    # When attached to a terminal, a "helpful" pager pops up.
    run('rvm install %(ruby_version)s' % locals(), pty=False)

def gemset(gemsetname, ruby_version=DEFAULT_RUBY_VERSION):
    """
    Ensure an rvm with this gemset exists, and return a context manager
    for executing commands in this gemset.

    Possible values for ``ruby_version`` are a string containing a ruby
    interpreter version, e.g. '1.9.2', or the string 'system' indicating
    the system's default (non-rvm-controlled) interpreter should be used.

    E.g.
        with rvm.gemset('production'):
            run('bundle install foolib')
    """
    if ruby_version != 'system':
        interpreter(ruby_version)
    return prefix('rvm use %(ruby_version)s@%(gemsetname)s --create' % locals())

#def install_gems_from_gemfile(gemfile_path):
    #"""
    #Install the dependencies of a Ruby app, which has its dependencies
    #specified in a Gemfile or Gemfile.lock.
    #``gemfile_path`` should be the path to the Gemfile or Gemfile.lock.

    #(Using a Gemfile.lock is advised: this is an exact dependency closure,
    #whereas a Gemfile will get you slightly different gem versions on each
    #install, in general.)
    #"""
    #with cd(os.path.dirname(gemfile_path)):
        #pass
