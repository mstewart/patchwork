from fabric.api import sudo

from patchwork import packages


MYSQL_CLIENT_DEPS = ['mysql-client']
MYSQL_SERVER_DEPS = ['mysql-server']


def client():
    """
    Require the mysql commandline client.
    """
    packages.deb.install(MYSQL_CLIENT_DEPS)


def server():
    """
    Require the mysql database server to be installed.
    """
    packages.deb.install(MYSQL_SERVER_DEPS)
    sudo('service mysql start')
