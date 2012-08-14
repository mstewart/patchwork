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


def query(statement, mysql_user=None, mysql_password=None, mysql_database=None):
    """
    Execute a SQL query against a mysql server running on the host.
    Non-idempotent in general (since it allows arbitrary queries).

        ``mysql_user``: The mysql user to run the query as.
        The query will be executed locally, so the account
        will be the ``mysql_user@localhost`` one.
        ``mysql_password``: Password for the specified user.
        If not specified, passwordless authentication is used.

    TODO: Put the password into a temporary mysql config file, instead of
    insecurely into the command line.
    TODO: Add support for alternative local sockets for connection.
    """
    # If parameters are not explicitly specified, get them from fabric's env,
    # or else fall back to defaults.
    if mysql_user is None:
        mysql_user = env.get(mysql_user, 'root')
    if mysql_password is None:
        mysql_password = env.get(mysql_password, None)
    if mysql_database is None:
        mysql_database = env.get(mysql_database, None)

    flags = ['--user=%s' % mysql_user]
    if mysql_database:
        flags.append('--database=%s' % mysql_database)
    if mysql_password:
        flags.append('--password=%s' % mysql_password)

    mysql_shell = """mysql --raw --batch %s --execute """ % " ".join(flags)
    with settings(shell=mysql_shell):
        return run(statement)


def remove_user(mysql_user_name, mysql_user_host, mysql_runas_user=None, mysql_password=None):
    """
    Ensure the given user account is not present.
    """
    query("""delete from mysql.user where User = '%(mysql_user_name)s' and Host = '%(mysql_user_host)s';""" % locals(),
            mysql_user=mysql_runas_user,
            mysql_password=mysql_password)


def can_login(mysql_user=None, mysql_password=None):
    """
    Check if the named mysql user can log in.
    """
    with settings(hide('everything'), warn_only=True):
        return query('', mysql_user=mysql_user, mysql_password=mysql_password).succeeded


def database(db_name, mysql_user=None, mysql_password=None):
    """
    Ensure a database with this name exists.

    Can also be used as a fabric context manager to specify which DB
    queries should run against, e.g.
        with database('development'):
            query('delete from user_login where user_id = 0;')
    """
    query("""create database if not exists %(db_name)s""" % locals(),
            mysql_user=mysql_user,
            mysql_password=mysql_password)
    return settings(mysql_database=db_name)