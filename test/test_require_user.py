from patchwork import require
import fabric

from unittest import TestCase
from mock import patch

@patch('patchwork.require.users.create')
@patch('patchwork.require.users.get_homedir')
@patch('patchwork.require.users.add_to_group')
@patch('patchwork.require.users.exists')
@patch('patchwork.require.users.directory')
class UserCommandsMockTestCase(TestCase):
    def test_require_new_user(self, directory, exists, add_to_group, get_homedir, create):
        name, home = 'myuser', '/myhome'
        exists.return_value = False

        require.user(name, home=home)
        create.assert_called_once_with(name, home=home)
        directory.assert_called_once_with(home, owner=name, runner=fabric.api.sudo)

    def test_require_existing_user_with_same_homedir(self, directory, exists, add_to_group, get_homedir, create):
        name, home = 'myuser', '/myhome'
        exists.return_value = True
        get_homedir.return_value = home

        require.user(name, home=home)
        self.assertFalse(create.called)

    def test_require_existing_user_with_same_homedir_but_different_slashes(self, directory, exists, add_to_group, get_homedir, create):
        name, home = 'myuser', '/home/myuser/'
        exists.return_value = True
        get_homedir.return_value = '/home/myuser'

        require.user(name, home=home)
        self.assertFalse(create.called)

    def test_require_user_different_homedir(self, directory, exists, add_to_group, get_homedir, create):
        name, home = 'myuser', '/myhome'
        exists.return_value = True
        get_homedir.return_value = '/home/someotherdir'

        with self.assertRaises(RuntimeError):
            require.user(name, home=home)
        self.assertTrue(create.is_called)

