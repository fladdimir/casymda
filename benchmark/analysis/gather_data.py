import pandas

# retrieve data relative to project root

data_paths = [
    "benchmark/results/CPython38.csv",
    "./benchmark/results/PyPy73.csv",
    "../csa4cs/Benchmark/results/results.csv",
    "../csa4j/benchmark/results_merged.csv",
]
result_path = "./benchmark/results/results.csv"

results = pandas.DataFrame()
for path in data_paths:
    read = pandas.read_csv(path, index_col=False)
    results = results.append(
        read,
    )
results.to_csv(result_path, index=False)
