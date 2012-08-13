
class PackageInstallationError(Exception):
    def __init__(self, msg):
        super(PackageInstallationError, self).__init__(msg)

class UnsupportedDistributionError(NotImplementedError):
    def __init__(self, msg):
        super(UnsupportedDistributionError, self).__init__(msg)
