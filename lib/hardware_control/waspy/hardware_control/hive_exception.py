class HiveError(Exception):
    """ A base class for all service_mill related errors """
    pass


class InvalidDaemonError(HiveError):
    """ An exception for any hardware related requests"""
    pass


class AbortedError(HiveError):
    """ An exception for any hardware related requests"""
    pass


class FitError(HiveError):
    """ An exception for when fitting a curve over a list of 2D points fails"""
    pass

