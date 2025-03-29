import logging
import math
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

logging.basicConfig()

logger = logging.getLogger(__name__)


def integrate_part(f, a, step, start, end):
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


def worker(args):
    f, a, step, start, end = args
    return integrate_part(f, a, step, start, end)


def integrate_parallel(f, a, b, *, n_jobs=1, n_iter=10_000_000, executor_type='thread'):
    step = (b - a) / n_iter
    split_step = n_iter // n_jobs
    values = [(f, a, step, i * split_step, (i + 1) * split_step) for i in range(n_jobs)]
    executor_class = (ThreadPoolExecutor if executor_type == 'thread' else ProcessPoolExecutor)

    with executor_class(max_workers=n_jobs) as executor:
        results = executor.map(worker, values)
    return sum(results)


def benchmark():
    cpu_num = multiprocessing.cpu_count()
    jobs_range = list(range(1, cpu_num * 2))
    results = []

    for n_jobs in jobs_range:
        for executor_type in ['thread', 'process']:
            start_time = time.time()
            result = integrate_parallel(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_type=executor_type)
            elapsed_time = time.time() - start_time
            results.append(f"{executor_type}, {n_jobs}, {elapsed_time:.4f}")
            print(f"{executor_type}: n_jobs={n_jobs}, result={result:.6f}, time={elapsed_time:.4f}s")

    with open("artifacts/integration_benchmark.csv", "w") as f:
        f.write("executor_type,n_jobs,time\n")
        f.write("\n".join(results))


if __name__ == "__main__":
    benchmark()
