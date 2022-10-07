class IbaError(Exception):
    """ A base class for all iba related errors """
    pass


class FitError(IbaError):
    """ fitting a curve over a list of 2D points failed"""
    pass


class RangeError(IbaError):
    """ Invalid range specified"""
