import time

import functions_for_timer


# First timer (easy)


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


results = []


class Timer:
    def __init__(self):
        self._start_time = None
        self._counter = 1

    def start(self):

        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):

        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = round((time.perf_counter() - self._start_time), 4)
        self._start_time = None

        if self._counter > len(results):
            results.append([])
            results[self._counter - 1].append(elapsed_time)
            self._counter += 1

        else:
            results[self._counter - 1].append(elapsed_time)
            self._counter += 1


def easy_timer():
    t = Timer()
    t.start()
    a = functions_for_timer.get_historical_candles('1m')
    t.stop()

    t.start()
    b = functions_for_timer.get_historical_candles_1('1m')
    t.stop()


def repeater(n):
    for i in range(n):
        easy_timer()
        if i == n - 1:
            print(
                f'Avarage for first function for {i + 1} repetitions: {round(sum(results[0]) / len(results[0]), 5)} \n'
                f'Avarage for second function for {i + 1} repetitions: {round(sum(results[1]) / len(results[1]), 5)}')
            print(f'Full time: {round(max(sum(results[0]), sum(results[1])), 4)} \n')


if __name__ == "__main__":
    repeater(5)
    repeater(10)
