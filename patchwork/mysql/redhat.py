from fabric.api import sudo

from patchwork import packages
import mysql
import logging


MYSQL_CLIENT_DEPS = ['mysql']
MYSQL_SERVER_DEPS = ['mysql-server']


def client(*args, **kwargs):
    """
    Require the mysql commandline client.
    """
    packages.rpm.install(MYSQL_CLIENT_DEPS)


def server(mysql_root_password=None, *args, **kwargs):
    """
    Require the mysql database server to be installed.

    TODO: Set root password in a more secure way than issuing it in a 
    command line.
    Put a change password query in a temporary file, then run the file?
    """
    packages.rpm.install(MYSQL_SERVER_DEPS)
    sudo('service mysqld start')

    # A couple possibilities we need to consider to make this idempotent:
    # 1) Fresh mysql install: no password set
    # 2) Installer already run: root password will already be set correctly,
    # we can continue and complete the operation successfully
    # 3) Different password set: bail out.
    no_password_set = mysql.can_login('root')
    password_already_set = mysql.can_login('root', mysql_password=mysql_root_password)

    if no_password_set:
        if mysql_root_password:
            logging.debug('mysql root password unset: setting it now.')
            sudo("mysqladmin -u root password '%s'" % mysql_root_password)
    elif password_already_set:
        logging.debug('mysqld root password already set to desired value.')
    else:
        msg = 'mysqld root password set to an unknown value. Cannot continue mysqld setup.'
        logging.error(msg)
        raise mysql.MysqlAuthenticationError(msg)

    # Initial state on package install: no root password, anonymous accounts,
    # and test databases.
    # Remove all users other than 'root'@'localhost' to start with:
    mysql.query("delete from mysql.user where User <> 'root' or Host <> 'localhost';",
            mysql_password=mysql_root_password)
    # Drop the "test" DB:
    sudo("mysqladmin -u root drop test")
