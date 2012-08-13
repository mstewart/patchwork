from patchwork import packages, mysql

from unittest import TestCase
from mock import patch

class MysqlInstallationTest(TestCase):
    @patch('patchwork.packages.distro_family')
    @patch('patchwork.packages.install')
    def test_mysql_client_redhat_install(self, install, distro_family):
        distro_family.return_value = 'redhat'
        mysql.client()
        install.assert_called_once_with('mysql')

    @patch('patchwork.packages.distro_family')
    @patch('patchwork.packages.install')
    def test_mysql_server_debian_install(self, install, distro_family):
        distro_family.return_value = 'debian'
        mysql.server()
        install.assert_called_once_with('mysql-server')
