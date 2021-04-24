class BadMessage(Exception):
    """If the user's message is written in wrong format"""
    pass


class UserNotFound(Exception):
    """If person isn't in db"""
    pass


class NoInformationException(Exception):
    """When there is a user table but there aren't any rows"""
    pass