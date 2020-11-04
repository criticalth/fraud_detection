# Libraries
# Built-ins
import os
import time
import functools

# Third-party developed


def import_export(path, import_func, *dargs, **dkwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.isfile(path):
                print("Extract cache with function {}!".format(func.__name__))
                return import_func(*dargs, **dkwargs)
            else:
                print("Executing original function {}!".format(func.__name__))
                res = func(*args, **kwargs)
                res.to_csv(path, index=False)
                return res
        return wrapper
    return decorator


def time_execution(func):
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
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator
