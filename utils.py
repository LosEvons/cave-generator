import time
import os


def xy_to_i(x: int, y: int, width: int) -> int:
    """Converts an (x, y) coordinate to an int index in a one dimensional coordinate system."""
    return y * width + x


def i_to_xy(i: int, width: int) -> tuple[int, int]:
    """Converts an int index from a one dimensional coordinate system to an (x, y) coordinate."""
    return i % width, i // width


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