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

    @patch('patchwork.mysql.debian.sudo')
    @patch('patchwork.mysql.mysql.distro_family')
    @patch('patchwork.packages.deb')
    def test_mysql_server_debian_install(self, deb, distro_family, sudo):
        distro_family.return_value = 'debian'
        mysql.server()
        deb.install.assert_called_once_with(['mysql-server'])

class QueryTest(TestCase):
    @patch('patchwork.mysql.mysql.run')
    def test_query(self, run):
        mysql.query('SELECT 1;')
        run.assert_called_once_with("""mysql --raw --batch --execute 'SELECT 1;' --user=root""")

class AdminFunctionsTest(TestCase):
    @patch('patchwork.mysql.mysql.query')
    def test_remove_user(self, query):
        mysql.remove_user('user1', 'localhost')
        query.assert_called_once_with("delete from mysql.user where User = user1 and Host = localhost;",
                mysql_user='root',
                mysql_password=None)
