class NexusError(Exception):
    pass

class AuthenticationError(NexusError):
    pass

class CredentialsError(NexusError):
    pass
