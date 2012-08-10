from patchwork import require
import fabric

from unittest import TestCase
import mock

@mock.patch('patchwork.require.users.create')
@mock.patch('patchwork.require.users.get_homedir')
@mock.patch('patchwork.require.users.add_to_group')
@mock.patch('patchwork.require.users.exists')
@mock.patch('patchwork.require.users.directory')
class UserCommandsMockTestCase(TestCase):
    def test_require_new_user(self, directory, exists, add_to_group, get_homedir, create):
        exists.return_value = False
        name, home = 'myuser', '/myhome'
        require.user(name, home=home)
        create.assert_called_once_with(name, home=home)
        directory.assert_called_once_with(home, owner=name, runner=fabric.api.sudo)
