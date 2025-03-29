import multiprocessing
import threading
import time


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def run_sync(n, runs):
    times = []
    for _ in range(runs):
        _, elapsed = fib(n), time.time()
        times.append(elapsed)
    return sum(times)


def run_threads(n, runs):
    threads = []
    for _ in range(runs):
        t = threading.Thread(target=fib, args=(n,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def run_processes(n, runs):
    processes = []
    for _ in range(runs):
        p = multiprocessing.Process(target=fib, args=(n,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def main():
    n = 35
    runs = 10

    results = []
    print('run sync')
    t = time.time()
    run_sync(n, runs)
    results.append(f"Sync: {time.time() - t:.2f} sec")
    t = time.time()
    print('run threads')
    run_threads(n, runs)
    results.append(f"Threads: {time.time() - t:.2f} sec")
    t = time.time()
    print('run process')
    run_processes(n, runs)
    results.append(f"Processes: {time.time() - t:.2f} sec")

    with open("artifacts/fib_benchmark.txt", "w") as f:
        f.write("\n".join(results) + "\n")

    print("Результаты записаны в fib_benchmark.txt")


if __name__ == "__main__":
    main()
