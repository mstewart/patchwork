from fabric.api import run

def directory(path, owner='', group='', mode='', runner=run):
    """
    Require a directory to exist with the specified attributes.
    """
    if runner is None:
        runner = run
    if not is_dir(path):
        runner('mkdir -p "%(path)s"' % locals())
    if owner or group:
        runner('chown %(owner)s:%(group)s "%(path)s"' % locals())
    if mode:
        runner('chmod %(mode)s "%(path)s"' % locals())