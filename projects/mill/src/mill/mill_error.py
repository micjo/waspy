class MillError(Exception):
    """ A base class for all mill related errors """
    pass


class CancelledError(MillError):
    """An exception for when a job is cancelled"""
    pass
