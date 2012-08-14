import fabric
from fabric.context_managers import settings
from patchwork import packages, mysql

from unittest import TestCase
from mock import patch

class MysqlInstallationTest(TestCase):
    @patch('patchwork.mysql.mysql.distro_family')
    @patch('patchwork.packages.rpm')
    def test_mysql_client_redhat_install(self, rpm, distro_family):
        distro_family.return_value = 'redhat'
        mysql.client()
        rpm.install.assert_called_once_with(['mysql'])

    @patch('patchwork.mysql.mysql.distro_family')
    @patch('patchwork.packages.deb')
    def test_mysql_client_debian_install(self, deb, distro_family):
        distro_family.return_value = 'debian'
        mysql.client()
        deb.install.assert_called_once_with(['mysql-client'])

    @patch('patchwork.mysql.debian.sudo')
    @patch('patchwork.mysql.mysql.distro_family')
    @patch('patchwork.packages.deb')
    def test_mysql_server_debian_install(self, deb, distro_family, sudo):
        distro_family.return_value = 'debian'
        mysql.server()
        deb.install.assert_called_once_with(['mysql-server'])

    @patch('patchwork.mysql.mysql.query')
    @patch('patchwork.mysql.redhat.sudo')
    @patch('patchwork.mysql.mysql.distro_family')
    @patch('patchwork.packages.rpm')
    def test_mysql_server_redhat_install(self, rpm, distro_family, sudo, query):
        distro_family.return_value = 'redhat'
        mysql.server()
        rpm.install.assert_called_once_with(['mysql-server'])

class QueryTest(TestCase):
    @patch('patchwork.mysql.mysql.run')
    def test_query(self, run):
        prev_shell = fabric.api.env.shell
        mysql.query('SELECT 1;')
        run.assert_called_once_with("SELECT 1;")
        self.assertIn('bash', fabric.api.env.shell)
        self.assertEqual(prev_shell, fabric.api.env.shell)

class AdminTest(TestCase):
    @patch('patchwork.mysql.mysql.query')
    def test_remove_user(self, query):
        mysql.remove_user('user1', 'localhost')
        query.assert_called_once_with("delete from mysql.user where User = 'user1' and Host = 'localhost';",
                mysql_user=None,
                mysql_password=None)

