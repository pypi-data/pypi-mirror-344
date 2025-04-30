import contextlib
import time


@contextlib.contextmanager
def timer() -> float:
    start = time.perf_counter()
    yield lambda: time.perf_counter() - start
