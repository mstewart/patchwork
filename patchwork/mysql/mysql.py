from fabric.api import *

import redhat, debian
from patchwork.info import distro_family


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

        ``mysql_user``: The mysql user to run the query as.
        The query will be executed locally, so the account
        will be the ``mysql_user@localhost`` one.
        Defaults to ``root``.
        ``mysql_password``: Password for the specified user.
        If not specified, passwordless authentication is used.

    TODO: Put the password into a temporary mysql config file, instead of
    insecurely into the command line.
    TODO: Add support for fabric env entries for configuration.
    """
    if mysql_user is None:
        mysql_user = 'root'
    flags = ['--user=%s' % mysql_user]
    if mysql_database:
        flags.append('--database=%s' % mysql_database)
    if mysql_password:
        flags.append('--password=%s' % mysql_password)
    flag_string = " ".join(flags)
    run("""mysql --raw --batch --execute '%(statement)s' %(flag_string)s""" % locals())
