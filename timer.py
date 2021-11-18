import time

import functions_for_timer


# First timer (easy)

def easy_timer():
    tic = time.perf_counter()
    a = functions_for_timer.get_historical_candles('1m')
    toc = time.perf_counter()
    print(f'Getting all candles in {toc - tic:0.4f} seconds')


if __name__ == "__main__":
    easy_timer()
