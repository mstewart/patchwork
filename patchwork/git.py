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
    return show_toplevel.succeeded and show_toplevel.stdout == repo_path


def clone(source_url, destination_repo_path=None, runner=None):
    """
    Clone a git repo from the ``source_url`` to ``destination_repo_path``.
    """
    if runner is None:
        runner = run
    runner("git clone %s %s" % (source_url, destination_repo_path))


def pull(source_repo_url, destination_repo_path, runner=None):
    """
    Pull from the git repo at ``source_repo_url`` into the repository at
    ``destination_repo_path``.
    """
    if runner is None:
        runner = run
    with cd(destination_repo_path):
        runner("git pull %s" % source_repo_url)
    
def repo(source_repo, destination_path, runner=None):
    """
    Ensure that an up-to-date git repo is in place at ``destination_path``,
    cloning or pulling from ``source_repo`` as necessary.
    """
    if runner is None:
        runner = run
    if is_git_repo(destination_path):
        pull(source_repo, destination_path)
    else:
        clone(source_repo, destination_path)
