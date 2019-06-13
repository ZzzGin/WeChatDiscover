class UserNameQueryError(Exception):
    def __init__(self, message):
        self.message = message

class AddWorkError(Exception):
    def __init__(self, message):
        self.message = message

class CacheKeyError(Exception):
    def __init__(self, message):
        self.message = message
        