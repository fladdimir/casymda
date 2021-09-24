# benchmark

simple sample model to compare execution times:

## execution

activate corresponding environment

python benchmark/model/run_benchmark.py
(overwrites previous results)

python benchmark/analysis/gather_data.py  
python benchmark/analysis/plot.py

## configuration

see [run_benchmark_test.py](./model/run_benchmark_test.py)

configurable number of created entities (longer runs) and inter-arrival-time (impacts number of simultaneously simulated entities)
