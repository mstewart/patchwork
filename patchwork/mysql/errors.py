from ..errors import AuthenticationError


class MysqlQueryError(SystemExit):
    """
    Mysql query error.

    Why subclass SystemExit?  Because that's de-facto the exception raised
    by a normal fabric.api.run() failure.
    """
    def __init__(self, msg):
        super(MysqlQueryError, self).__init__(msg)


class MysqlAuthenticationError(AuthenticationError):
    def __init__(self, msg):
        super(MysqlAuthenticationError, self).__init__(msg)

