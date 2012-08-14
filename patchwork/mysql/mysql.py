from fabric.api import *

import redhat, debian
from patchwork.info import distro_family
from ..errors import AuthenticationError


class MysqlAuthenticationError(AuthenticationError):
    def __init__(self, msg):
        super(MysqlAuthenticationError, self).__init__(msg)


def _implementor():
    """
    Return the module implementing mysql operations for the
    current distro.
    """
    mappings = {
            'redhat': redhat,
            'debian': debian
            }
    family = distro_family()
    try:
        return mappings[family]
    except KeyError:
        raise UnsupportedDistributionError('System type detected as "' + family +
                '"; mysql management not implemented for this type.')


def client(*args, **kwargs):
    return _implementor().client(*args, **kwargs)


def server(*args, **kwargs):
    return _implementor().server(*args, **kwargs)


def query(statement, mysql_user='root', mysql_password=None, mysql_database=None):
    """
    Execute a SQL query against a mysql server running on the host.

        ``mysql_user``: The mysql user to run the query as.
        The query will be executed locally, so the account
        will be the ``mysql_user@localhost`` one.
        ``mysql_password``: Password for the specified user.
        If not specified, passwordless authentication is used.

    TODO: Put the password into a temporary mysql config file, instead of
    insecurely into the command line.
    TODO: Add support for fabric env entries for configuration.
    TODO: Add support for alternative local sockets for connection.
    """
    flags = ['--user=%s' % mysql_user]
    if mysql_database:
        flags.append('--database=%s' % mysql_database)
    if mysql_password:
        flags.append('--password=%s' % mysql_password)
    flag_string = " ".join(flags)
    mysql_shell = """mysql --raw --batch %(flag_string)s --execute """ % locals()
    with settings(shell=mysql_shell):
        return run(statement)


def remove_user(mysql_user_name, mysql_user_host, mysql_runas_user='root', mysql_password=None):
    query("""delete from mysql.user where User = '%(mysql_user_name)s' and Host = '%(mysql_user_host)s';""" % locals(),
            mysql_user=mysql_runas_user,
            mysql_password=mysql_password)


def can_login(mysql_user='root', mysql_password=None):
    with settings(hide('everything'), warn_only=True):
        return query('', mysql_user=mysql_user, mysql_password=mysql_password).succeeded

