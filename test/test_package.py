from patchwork import packages

from unittest import TestCase
from mock import patch

class PackageDelegationTest(TestCase):
    @patch('patchwork.packages.distro_family')
    @patch('patchwork.packages.rpm')
    def test_redhat_delegation(self, rpm, distro_family):
        distro_family.return_value = 'redhat'
        packages.install('mypkg')
        rpm.install.assert_called_once_with('mypkg')

    @patch('patchwork.packages.distro_family')
    @patch('patchwork.packages.deb')
    def test_debian_delegation(self, deb, distro_family):
        distro_family.return_value = 'debian'
        packages.install('mypkg')
        deb.install.assert_called_once_with('mypkg')

    @patch('patchwork.packages.distro_family')
    def test_unknown_delegation(self, distro_family):
        distro_family.return_value = 'other'
        with self.assertRaises(NotImplementedError):
            packages.install('mypkg')

class PackageQueryTest(TestCase):
    @patch('patchwork.packages.rpm.sudo')
    @patch('patchwork.packages.rpm.run')
    def test_redhat_unary_query(self, run, sudo):
        for answer in (True, False):
            run.reset_mock()
            run.return_value.succeeded = answer
            self.assertEqual(answer, packages.rpm.is_installed('mypkg'))
            run.assert_called_once_with('rpm --query --quiet mypkg')

    @patch('patchwork.packages.rpm.run')
    def test_redhat_multiple_query(self, run):
        packages.rpm.is_installed('mypkg1', 'mypkg2')
        run.assert_called_once_with('rpm --query --quiet mypkg1 mypkg2')

    @patch('patchwork.packages.deb.sudo')
    @patch('patchwork.packages.deb.run')
    def test_debian_unary_query(self, run, sudo):
        for answer in (True, False):
            run.reset_mock()
            run.return_value.succeeded = answer
            self.assertEqual(answer, packages.deb.is_installed('mypkg'))
            run.assert_called_once_with('dpkg-query --show mypkg')

    @patch('patchwork.packages.deb.run')
    def test_debian_multiple_query(self, run):
        packages.deb.is_installed('mypkg1', 'mypkg2')
        run.assert_called_once_with('dpkg-query --show mypkg1 mypkg2')
