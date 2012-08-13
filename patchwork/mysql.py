import packages
import info

MYSQL_CLIENT_DEPS = {
        'debian': ['mysql-client'],
        'redhat': ['mysql']
}

MYSQL_SERVER_DEPS = {
        'debian': ['mysql-server'],
        'redhat': ['mysql-server']
}

def client():
    """
    Require the mysql commandline client.
    """
    packages.multi_distro_install(MYSQL_CLIENT_DEPS)

def server():
    """
    Require the mysql database server to be installed.
    """
    packages.multi_distro_install(MYSQL_SERVER_DEPS)
