import time

import functions_for_timer

# First timer (easy)

results = [[], []]


def easy_timer():
    tic = time.perf_counter()
    a = functions_for_timer.get_historical_candles('1m')
    toc = time.perf_counter()

    tic1 = time.perf_counter()
    b = functions_for_timer.get_historical_candles_1('1m')
    toc1 = time.perf_counter()

    result1 = round((toc - tic), 4)
    result2 = round((toc1 - tic1), 4)
    results[0].append(result1)
    results[1].append(result2)


if __name__ == "__main__":
    for i in range(25):
        easy_timer()

    print(f'Avarage for first function: {sum(results[0])/len(results[0])} \n'
          f'Avarage for second function: {sum(results[1])/len(results[1])}')

