import matplotlib.pyplot as plt

def plot_comparative_graph(fifo_steps, lru_steps, optimal_steps, fifo_faults, lru_faults, optimal_faults, title="Graph"):
    """Plot a comparative graph with page numbers starting from 1 and data point annotations."""
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Page Numbers")

    # Prepare data for plotting
    fifo_data = [step[-1] for step in fifo_steps if len(step) > 0]
    lru_data = [step[-1] for step in lru_steps if len(step) > 0]
    optimal_data = [step[-1] for step in optimal_steps if len(step) > 0]

    # Generate x-axis values (starting from 1)
    steps_fifo = range(1, len(fifo_data) + 1)
    steps_lru = range(1, len(lru_data) + 1)
    steps_optimal = range(1, len(optimal_data) + 1)

    # Plot data with pointers
    ax.plot(steps_fifo, fifo_data, label=f"FIFO Faults: {fifo_faults}", color="blue", marker="o")
    ax.plot(steps_lru, lru_data, label=f"LRU Faults: {lru_faults}", color="red", marker="o")
    ax.plot(steps_optimal, optimal_data, label=f"Optimal Faults: {optimal_faults}", color="green", marker="o")

    # Annotate data points
    for x, y in zip(steps_fifo, fifo_data):
        ax.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)
    for x, y in zip(steps_lru, lru_data):
        ax.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)
    for x, y in zip(steps_optimal, optimal_data):
        ax.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)

    ax.legend()
    plt.show()


def plot_individual_graph(steps, faults, title="Page Replacement Simulation"):
    """Plot an individual graph with page numbers starting from 1 and data point annotations."""
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Page Numbers")

    # Prepare data for plotting
    data = [step[-1] for step in steps if len(step) > 0]

    # Generate x-axis values (starting from 1)
    x_values = range(1, len(data) + 1)

    # Plot data with pointers
    ax.plot(x_values, data, label=f"Page Faults: {faults}", color="blue", marker="o")

    # Annotate data points
    for x, y in zip(x_values, data):
        ax.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)

    ax.legend()
    plt.show()
