from fabric.api import sudo, run
from fabric.contrib.files import exists

from ..users import *
from files import directory
from os.path import normpath

def user(name, home=None, groups=None):
    """
    Require a user to exist, having each of the specified set of
    groups as its supplemental groups.
    The user's primary gid will be a new user-specific group.

    If the user already exists, ensure it has *at least* the specified
    set of supplemental groups.  Extra group memberships will not be removed.

    If the user already exists, ensure it has the specified homedir.
    Error out if this is not the case (as changing the homedir of a
    possibly in-use user is pretty dangerous, won't update environment
    variables for running processes, will be refused on Linux systems, etc.
    It's also a pretty strong sign that the system is in an unexpected
    state and requires manual attention.)
    """
    if not exists(name):
        create(name, home=home)
    elif home:
        observed_home = get_homedir(name)
        if not normpath(observed_home) == normpath(home):
            raise UserCreationError("User %s already exists with homedir %s (expected %s)" %
                    (name, observed_home, home))
    if home:
        directory(home, owner=name, runner=sudo)
    if groups:
        for group in groups:
            add_to_group(name, group)
