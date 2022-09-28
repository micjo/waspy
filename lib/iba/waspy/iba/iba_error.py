class IbaError(Exception):
    """ A base class for all iba related errors """
    pass


class FitError(IbaError):
    """ An exception for when fitting a curve over a list of 2D points fails"""
    pass

