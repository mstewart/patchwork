from patchwork import user
import fabric

import os, pwd

from unittest import TestCase

import mock

def local_run(*args, **kwargs):
    """Runner wrapper for executing a command locally, and capturing its
    output much like api.run() or sudo() do."""
    kwargs['capture']=True
    return fabric.api.local(*args, **kwargs)

class UserCommandsMockTestCase(TestCase):
    @mock.patch('patchwork.user.run')
    def test_user_exists_mock(self, run):
        for retval in (True, False):
            run.reset_mock()
            run.return_value.succeeded = retval
            self.assertEqual(retval, user.exists('foo'))
            run.assert_called_once_with('getent passwd foo')

    @mock.patch('patchwork.user.exists')
    @mock.patch('patchwork.user.run')
    def test_homedir_nonexistent_user(self, run, exists):
        exists.return_value = False
        with self.assertRaises(RuntimeError):
            user.get_homedir('someuser')


class UserLocalCommandsTestCase(TestCase):
    """Running non-invasive commands locally"""

    @mock.patch('patchwork.user.run', local_run)
    def test_user_exists_local(self):
        current_user = pwd.getpwuid(os.getuid()).pw_name
        self.assertTrue(user.exists(current_user))

    @mock.patch('patchwork.user.run', local_run)
    def test_user_does_not_exist_local(self):
        illegal_user_name = 'z::f' # colons are disallowed in usernames
        self.assertFalse(user.exists(illegal_user_name))

    @mock.patch('patchwork.user.run', local_run)
    def test_homedir_local(self):
        current_pw = pwd.getpwuid(os.getuid())
        self.assertEqual(current_pw.pw_dir, user.get_homedir(current_pw.pw_name))

