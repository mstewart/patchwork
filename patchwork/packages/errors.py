
class PackageInstallationError(Exception):
    def __init__(self, msg):
        super(PackageInstallationError, self).__init__(msg)
