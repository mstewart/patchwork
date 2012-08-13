from patchwork import packages
from patchwork.packages import UnsupportedDistributionError

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

class MultiDistroInstallationTest(TestCase):
    @patch('patchwork.packages.distro_family')
    @patch('patchwork.packages.install')
    def test_package_mapping(self, install, distro_family):
        pkgs = { 'debian': ['deb1', 'deb2'],
                'redhat': ['rpm1', 'rpm2'] }
        distro_family.return_value = 'debian'
        packages.multi_distro_install(pkgs)
        install.assert_called_once_with(*pkgs['debian'])
        
    @patch('patchwork.packages.distro_family')
    @patch('patchwork.packages.install')
    def test_no_packages_mapped(self, install, distro_family):
        pkgs = { 'debian': ['deb1', 'deb2'],
                'redhat': ['rpm1', 'rpm2'] }
        distro_family.return_value = 'arch'
        with self.assertRaises(UnsupportedDistributionError):
            packages.multi_distro_install(pkgs)
        self.assertFalse(install.called)

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
