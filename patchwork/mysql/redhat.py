from fabric.api import sudo

from patchwork import packages


MYSQL_CLIENT_DEPS = ['mysql']
MYSQL_SERVER_DEPS = ['mysql-server']


def client(*args, **kwargs):
    """
    Require the mysql commandline client.
    """
    packages.rpm.install(MYSQL_CLIENT_DEPS)


def server(*args, **kwargs):
    """
    Require the mysql database server to be installed.
    """
    packages.rpm.install(MYSQL_SERVER_DEPS)
    sudo('service mysqld start')
