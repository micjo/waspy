class IbaError(Exception):
    """ A base class for all iba related errors """
    pass


class FitError(IbaError):
    """ fitting a curve over a list of 2D points failed"""
    pass


class CancelError(IbaError):
    """ Operation was cancelled"""
    pass

class RangeError(IbaError):
    """ Invalid range specified"""
    pass


class ErdParamsMissingError(IbaError):
    """Missing Erd conversion params"""
    pass
