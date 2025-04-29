import time
from PIL import Image
from contextlib import ContextDecorator


class PerfCounter(ContextDecorator):
    """
    Context manager and decorator to measure elapsed time.

    Usage as a context manager:
        with PerfCounter():
            ...  # code to time

    Usage as a decorator:
        @PerfCounter()
        def foo(...):
            ...

    The elapsed time is printed on exit.
    """
    def __init__(self) -> None:
        self.start = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end = time.perf_counter()
        self.elapsed = end - self.start


def pillow_image_extensions():
    Image.init()
    return {
        ext.lower()
        for ext, fmt in Image.registered_extensions().items()
        if (
            fmt in Image.OPEN
            and Image.MIME.get(fmt, "").startswith("image/")
        )
    }
