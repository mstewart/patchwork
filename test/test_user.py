from patchwork import users
import fabric
import os, pwd

from unittest import TestCase
from mock import patch

def local_run(*args, **kwargs):
    """Runner wrapper for executing a command locally, and capturing its
    output much like api.run() or sudo() do."""
    kwargs['capture']=True
    return fabric.api.local(*args, **kwargs)

class UserCommandsMockTestCase(TestCase):
    @patch('patchwork.users.run')
    def test_user_exists_mock(self, run):
        for retval in (True, False):
            run.reset_mock()
            run.return_value.succeeded = retval
            self.assertEqual(retval, users.exists('foo'))
            run.assert_called_once_with('getent passwd foo')

    @patch('patchwork.users.exists')
    @patch('patchwork.users.run')
    def test_homedir_nonexistent_user(self, run, exists):
        exists.return_value = False
        with self.assertRaises(users.UserDoesNotExistError):
            users.get_homedir('someuser')

    @patch('patchwork.users.sudo')
    def test_add_to_group(self, sudo):
        users.add_to_group('myuser', 'mygroup')
        sudo.assert_called_once_with('usermod -G "mygroup" --append "myuser"')

    @patch('patchwork.users.sudo')
    def test_user_create(self, sudo):
        users.create('myuser', system=True, home='/tmp')
        sudo.assert_called_once_with('useradd --home "/tmp" --system --user-group myuser')

@patch('patchwork.users.run', local_run)
class UserLocalCommandsTestCase(TestCase):
    """Running non-invasive commands locally"""
    def test_user_exists_local(self):
        current_user = pwd.getpwuid(os.getuid()).pw_name
        self.assertTrue(users.exists(current_user))

    def test_user_does_not_exist_local(self):
        illegal_user_name = 'z::f' # colons are disallowed in usernames
        self.assertFalse(users.exists(illegal_user_name))

    def test_homedir_local(self):
        current_pw = pwd.getpwuid(os.getuid())
        self.assertEqual(current_pw.pw_dir, users.get_homedir(current_pw.pw_name))

