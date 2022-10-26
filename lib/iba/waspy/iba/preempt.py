import logging


'''
A safe way to interrupt and cancel functions in an object. A cancelled function is never run, a function that is 
interrupted, is stopped during its operation. This allows for proper exception handling and does not require async calls 
in your entire code base.

Using this requires to define cancel and use yield to indicate when it is safe for the function to relinquish control.
Using yield is not mandatory. Without yield the cancellation check only happens at the start


Example usage:
class SlowCall(object):
    cancel: bool

    def __init__(self):
        self.cancel = False

    @cancel_func
    def wait(self):
        for _ in range(10):
            print("SlowCall.wait")
            time.sleep(1)
            yield
 '''


def cancel_function(func, *args, **kw):
    saved_args = locals()
    logging.info("Function '" + str(saved_args) + "' cancelled")


def preemptive(func):
    def wrapper(self, *args, **kwargs):
        if self._cancel:
            cancel_function(func, *args, **kwargs)
        else:
            try:
                for _ in func(self, *args, **kwargs):
                    if self._cancel:
                        cancel_function(func, *args, **kwargs)
                        break
            except TypeError:
                pass
    return wrapper
