
class UnexpectedSystemStateError(Exception):
    def __init__(self, msg):
        super(UnexpectedSystemStateError, self).__init__(msg)

class AuthenticationError(UnexpectedSystemStateError):
    def __init__(self, msg):
        super(AuthenticationError, self).__init__(msg)
