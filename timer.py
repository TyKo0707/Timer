import time
import matplotlib.pyplot as plt
import functions_async
import functions_manual


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

        elapsed_time = round((time.perf_counter() - self._start_time), 8)
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
    a = functions_async.get_historical_candles('1m')
    t.stop()

    t.start()
    b = functions_manual.get_historical_candles('1m')
    t.stop()


x_es = [0]
y1_es = [0]
y2_es = [0]


def repeater(n):
    x_es.append(n)
    for i in range(n):
        easy_timer()
        if i == n - 1:
            avg1 = round(sum(results[0]) / len(results[0]), 8)
            y1_es.append(avg1)
            avg2 = round(sum(results[1]) / len(results[1]), 8)
            y2_es.append(avg2)
            print(
                f'Avarage for first function for {i + 1} repetitions: {avg1} \n'
                f'Avarage for second function for {i + 1} repetitions: {avg2}')
            print(f'Full time: {round(max(sum(results[0]), sum(results[1])), 8)} \n')


def build_graphic():
    l = 2.54 * max(x_es)
    h = 2.54 * max(max(y1_es), max(y2_es))
    plt.figure(figsize=(int(l), int(h)))
    plt.plot(x_es, y1_es, label="async", lw=3)
    plt.plot(x_es, y2_es, label="manual", lw=3)
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    repeater(1)
    repeater(2)
    repeater(3)
    repeater(4)
    repeater(5)
    build_graphic()
