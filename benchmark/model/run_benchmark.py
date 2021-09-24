import sys

sys.path.append(".")

import time
import sys

import benchmark.model.model as model_module
import pandas
from simpy import Environment

RESULTS_DIR = "./benchmark/results/"

runtime = (
    "Casymda@SimPy(PyPy73)" if "PyPy" in sys.version else "Casymda@SimPy(CPython38)"
)  # to be changed
n_entities = [10, 100, 1000, 10_000, 50_000, 100_000, 200_000]  # ~1 min i5
inter_arrival_times = [0, 10]


def run_benchmark():
    # warmup run?
    results = []
    for n_entity in n_entities:
        for iat in inter_arrival_times:
            sequential_proc_time = 10
            overall_seq_time = iat + (n_entity / 2) * sequential_proc_time
            last_time = (n_entity - 1) * iat + sequential_proc_time
            expected_end = max(last_time, overall_seq_time)
            t = run(
                max_entities=n_entity,
                inter_arrival_time=iat,
                sequential_proc_time=sequential_proc_time,
                expected_end=expected_end,
            )
            result = {
                "runtime": runtime,
                "n_entities": n_entity,
                "inter_arrival_time": iat,
                "time": t,
            }
            results.append(result)
    pandas.DataFrame(results).to_csv(RESULTS_DIR + runtime + ".csv", index=False)


def run(
    max_entities=10,
    inter_arrival_time=0,
    parallel_proc_time=10,
    sequential_proc_time=10,
    expected_end=50,
) -> float:

    model = model_module.Model(Environment())

    model.source.max_entities = max_entities
    model.source.inter_arrival_time = inter_arrival_time

    model.parallel_proc.process_time = parallel_proc_time
    model.sequential_proc.process_time = sequential_proc_time

    t0 = time.time()
    model.env.run()
    t = time.time() - t0

    assert model.sink.overall_count_in == model.source.overall_count_in
    assert model.parallel_proc.overall_count_in == model.source.max_entities / 2
    assert model.sequential_proc.overall_count_in == model.source.max_entities / 2
    assert model.env.now == expected_end

    return t


if __name__ == "__main__":
    run_benchmark()
