"""
Fabric tools for managing cloning/syncing from git repositories.
"""

from fabric.api import run
from fabric.context_managers import cd, settings, hide

def is_git_repo(repo_path, runner=None):
    """
    Check whether the given directory corresponds to a git repo.

    (Specifically, whether the directory is the top-level of a repo's working
    tree; bare repos don't count.)
    """
    if runner is None:
        runner = run
    with settings(hide('everything'), warn_only=True):
        with cd(repo_path):
            show_toplevel = runner('git rev-parse --show-toplevel')
    return show_toplevel.succeeded and show_toplevel.stdout == repo_path:


def clone(source_url, destination_repo_path=None, runner=None):
    """
    Clone a git repo from the given URL to destination_repo_path.

    If ``destination_repo_path`` is not specified, a repository will be
    created under the working directory (as is the default for ``git clone``).
    """
    if runner is None:
        runner = run
    cmd = "git clone %s" % source_url
    if destination_repo_path:
        cmd += " %s" % destination_repo_path
    runner(cmd)


def pull(source_repo_url, destination_repo_path, runner=None):
    """
    Pull from the source repo into the repository at destination_repo_path.
    """
    if runner is None:
        runner = run
    with cd(destination_repo_path):
        runner("git pull %s" % source_repo_url)
    
