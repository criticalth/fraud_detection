# Libraries
# Built-ins
import os
import time
import functools

# Third-party developed


# In-project development


def import_export(file,
        import_func=None, import_specs=dict(),
        export_func=None, export_specs=dict()
    ):
    """ Decorator generator for importing if result of a function already exists
        and exporting it if it does not.

    :param file: str, output file to save results or import from
    :param import_func: function, import function
    :param import_specs: tuple of args, additional import function arguments
    :param export_func: function, export function
    :param export_specs: tuple of args, additional export function arguments
    :return: decorator
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.isfile(file):
                print(f"Extract cache with function {func.__name__!r}!")
                return import_func(file, **import_specs)
            else:
                print(f"Execute original function {func.__name__!r}!")
                res = func(*args, **kwargs)
                print(f"Export results from function {func.__name__!r}!")
                export_func(res, file, **export_specs)
                return res
        return wrapper
    return decorator


def time_execution(func):
    """ A decorator to time a functions execution.
        The result is only a print stating running time in minutes.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = (end_time - start_time) / 60
        print(f"Finished {func.__name__!r} in {run_time:.1f} minutes")
        return value
    return wrapper_timer


def add_method(cls):
    """ A decorator that adds a function as a method to an existing class.
        NB: Existing to the module in which the function is being defined.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator
