from patchwork import packages, mysql

from unittest import TestCase
from mock import patch

class MysqlInstallationTest(TestCase):
    @patch('patchwork.packages.distro_family')
    @patch('patchwork.packages.rpm')
    def test_redhat_delegation(self, rpm, distro_family):
        distro_family.return_value = 'redhat'
        packages.install('mypkg')
        rpm.install.assert_called_once_with('mypkg')
