class HiveError(Exception):
    """ A base class for all hive related errors """
    pass


class InvalidDaemonError(HiveError):
    """ An exception for any hardware related requests"""
    pass


class AbortedError(HiveError):
    """ An exception for any hardware related requests"""
    pass
