class MillError(Exception):
    """ A base class for all mill related errors """
    pass


class AbortedError(MillError):
    """An exception for when a job is aborted"""
    pass
