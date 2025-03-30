import matplotlib.pyplot as plt
import matplotlib.animation as animation

def calculate_fifo(page_reference, frame_count):
    """Simulate FIFO Page Replacement Algorithm."""
    frames = []
    page_faults = 0
    fifo_queue = []

    steps = []
    for page in page_reference:
        if page not in fifo_queue:
            page_faults += 1
            if len(fifo_queue) < frame_count:
                fifo_queue.append(page)
            else:
                fifo_queue.pop(0)
                fifo_queue.append(page)
        frames.append(fifo_queue.copy())
        steps.append(frames[-1].copy())

    return steps, page_faults

def calculate_lru(page_reference, frame_count):
    """Simulate LRU Page Replacement Algorithm."""
    frames = []
    page_faults = 0
    recent_usage = []

    steps = []
    for page in page_reference:
        if page not in recent_usage:
            page_faults += 1
            if len(recent_usage) < frame_count:
                recent_usage.append(page)
            else:
                recent_usage.pop(0)
                recent_usage.append(page)
        else:
            recent_usage.remove(page)
            recent_usage.append(page)

        frames.append(recent_usage.copy())
        steps.append(frames[-1].copy())

    return steps, page_faults

def calculate_optimal(page_reference, frame_count):
    """Simulate Optimal Page Replacement Algorithm."""
    frames = []
    page_faults = 0

    steps = []
    for i in range(len(page_reference)):
        page = page_reference[i]
        if page not in frames:
            page_faults += 1
            if len(frames) < frame_count:
                frames.append(page)
            else:
                future_usage = []
                for frame in frames:
                    if frame in page_reference[i + 1:]:
                        future_usage.append(page_reference[i + 1:].index(frame))
                    else:
                        future_usage.append(float('inf'))

                replace_index = future_usage.index(max(future_usage))
                frames[replace_index] = page

        steps.append(frames.copy())

    return steps, page_faults

def plot_comparative_graph(fifo_steps, lru_steps, optimal_steps, fifo_faults, lru_faults, optimal_faults, title="Graph"):
    """Plot a graph for comparative mode."""
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Page Numbers")

    fifo_line, = ax.plot([], [], label=f"FIFO Faults: {fifo_faults}", color="blue")
    lru_line, = ax.plot([], [], label=f"LRU Faults: {lru_faults}", color="red")
    optimal_line, = ax.plot([], [], label=f"Optimal Faults: {optimal_faults}", color="green")

    ax.legend()

    def init():
        fifo_line.set_data([], [])
        lru_line.set_data([], [])
        optimal_line.set_data([], [])
        return fifo_line, lru_line, optimal_line

    def update(frame):
        if frame < len(fifo_steps):
            fifo_line.set_data(range(frame + 1), [step[-1] for step in fifo_steps[: frame + 1]])
        if frame < len(lru_steps):
            lru_line.set_data(range(frame + 1), [step[-1] for step in lru_steps[: frame + 1]])
        if frame < len(optimal_steps):
            optimal_line.set_data(range(frame + 1), [step[-1] for step in optimal_steps[: frame + 1]])
        return fifo_line, lru_line, optimal_line

    ani = animation.FuncAnimation(fig, update, frames=max(len(fifo_steps), len(lru_steps), len(optimal_steps)), 
                                  init_func=init, blit=True, interval=500, repeat=False)
    plt.show()

def plot_individual_graph(steps, faults, title="Page Replacement Simulation"):
    """Plot a graph for individual mode."""
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Page Numbers")

    line, = ax.plot([], [], label=f"Page Faults: {faults}", color="blue")
    ax.legend()

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        if frame < len(steps):
            line.set_data(range(frame + 1), [step[-1] for step in steps[: frame + 1]])
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(steps), init_func=init, blit=True, interval=500, repeat=False)
    plt.show()
