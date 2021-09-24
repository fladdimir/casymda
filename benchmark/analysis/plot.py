import pandas
import matplotlib.pyplot as plt

results_csv = "benchmark/results/results.csv"

results = pandas.read_csv(results_csv)
print(results)

print("\nFiltered:\n")
inter_arrival_time = 10
results = results[results["inter_arrival_time"] == inter_arrival_time]
print(results)

grouped_results = results.groupby(["runtime"])  # , "inter_arrival_time"])

fig, ax = plt.subplots(figsize=(8, 6))
for label, df in grouped_results:
    df.plot(
        x="n_entities",
        y="time",
        ylabel="time [s]",
        xlabel="# of entities",
        ax=ax,
        label=label,
        # loglog=True,
        # logx=True,
        grid=True,
        linestyle="--",
        marker="o",
    )
plt.legend()
explanation = "queuing" if inter_arrival_time == 0 else "no queuing"
subtitle = f"inter-arrival time: {inter_arrival_time} ({explanation})"
plt.title("Execution time by number of entities for different runtimes\n" + subtitle)
plt.show()
