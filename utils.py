import time
import os

def timeit(method):
    """Decorator that prints a function's execution time when DEBUG=1 is set in the environment variables
    Returns method unmodified (does nothing) if DEBUG is not set to 1
    """
    if os.environ.get("DEBUG") != "1":
        return method
    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print(f"{method.__name__} timed {end - start} seconds")
        return result
    return timed