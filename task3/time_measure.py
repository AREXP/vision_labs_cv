import collections
import contextlib
import time


class BaseError(Exception):
    pass


class TimerError(BaseError):
    pass


class TimeStorage:
    def __init__(self):
        self._data = collections.defaultdict(float)

    def push_elapsed(self, scope_name, elapsed):
        self._data[scope_name] += elapsed

        max_key = '{}_max'.format(scope_name)
        min_key = '{}_min'.format(scope_name)

        self._data[max_key] = max(elapsed, self._data.get(max_key, elapsed))
        self._data[min_key] = min(elapsed, self._data.get(min_key, elapsed))

    def get_storage(self):
        return dict(self._data)


class Timer:
    def __init__(self):
        self._start = time.time()
        self._stop = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop = time.time()

    @property
    def result(self):
        if self._stop is None:
            raise TimerError('Time must be stopped')

        return self._stop - self._start


@contextlib.contextmanager
def time_context(time_storage, scope_name):
    try:
        with Timer() as timer:
            yield
    finally:
        time_key = '{}_time'.format(scope_name)
        time_storage.push_elapsed(time_key, timer.result)


def main():
    storage = TimeStorage()
    with time_context(storage, 'scope1'):
        time.sleep(0.5)
    with time_context(storage, 'scope2'):
        time.sleep(0.1)
    with time_context(storage, 'scope1'):
        time.sleep(0.7)
    with time_context(storage, 'scope2'):
        time.sleep(0.2)

    print('Elapsed: %s', storage.get_storage())

if __name__ == '__main__':
    main()
