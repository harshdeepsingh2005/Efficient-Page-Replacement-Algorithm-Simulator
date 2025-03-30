from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def validate_input(pages_str, frames_str):
    """Validate input for pages and frames."""
    try:
        # Validate pages
        pages = list(map(int, pages_str.split()))
        if not pages:
            messagebox.showerror("Input Error", "Please enter at least one page.")
            return None, None

        # Validate frames
        frames = int(frames_str)
        if frames <= 0:
            messagebox.showerror("Input Error", "Number of frames must be a positive integer.")
            return None, None

        return pages, frames

    except ValueError:
        messagebox.showerror("Input Error", "Invalid input format. Please enter space-separated integers for pages and a single integer for frames.")
        return None, None

def calculate_fifo(page_reference, frame_count):
    """Simulate FIFO Page Replacement Algorithm."""
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
        frames = fifo_queue.copy()
        steps.append(frames)
    return steps, page_faults

def calculate_lru(page_reference, frame_count):
    """Simulate LRU Page Replacement Algorithm."""
    frames = []
    page_faults = 0
    usage_order = []

    steps = []
    for page in page_reference:
        if page in frames:
            # Update usage order
            usage_order.remove(page)
            usage_order.append(page)
        else:
            # Page fault
            page_faults += 1
            if len(frames) < frame_count:
                frames.append(page)
                usage_order.append(page)
            else:
                # Replace LRU page
                lru_page = usage_order.pop(0)
                frames.remove(lru_page)
                frames.append(page)
                usage_order.append(page)
        steps.append(frames.copy())
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

def plot_comparative_graph(pages,fifo_steps, lru_steps, optimal_steps,
                           fifo_faults, lru_faults, optimal_faults,
                           title="Comparison of Page Replacement Algorithms"):
    """Plot comparative animation of three algorithms."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    plt.subplots_adjust(hspace=0.5)
    fig.suptitle(title, fontsize=14)

    # Configure axes
    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(0, len(fifo_steps))
        ax.set_ylim(0, max(pages)+1)
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Page Number")

    ax1.set_title(f"FIFO (Faults: {fifo_faults})", color='blue')
    ax2.set_title(f"LRU (Faults: {lru_faults})", color='orange')
    ax3.set_title(f"Optimal (Faults: {optimal_faults})", color='green')

    # Create initial empty plots
    plots = []
    for ax in [ax1, ax2, ax3]:
        plot = ax.plot([], [], 's-', markersize=8, linewidth=1)[0]
        plots.append(plot)

    def init():
        for plot1 in plots:
            plot1.set_data([], [])
        return plots

    def update(frame):
        for i, (algorithm_steps, plot1) in enumerate(zip([fifo_steps, lru_steps, optimal_steps], plots)):
            x = list(range(frame+1))
            y = [step[i % len(step)] if len(step) > 0 else 0
                 for i, step in enumerate(algorithm_steps[:frame+1])]
            plot1.set_data(x, y)
        return plots

    ani = animation.FuncAnimation(
        fig, update, frames=len(fifo_steps),
        init_func=init, blit=True, interval=500, repeat=False
    )
    plt.show()

def plot_individual_graph(pages,steps, faults, title="Page Replacement Simulation"):
    """Plot individual algorithm animation with frame visualization."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_title(f"{title} (Faults: {faults})")
    ax.set_xlabel("Time Steps")
    ax.set_ylabel("Page Number")
    ax.set_ylim(0, max(pages)+1)
    ax.set_xlim(0, len(steps))

    # Create multiple lines for each frame slot
    lines = [ax.plot([], [], 's-', label=f'Frame {i+1}')[0]
             for i in range(len(steps[0]) if steps else 0)]

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def update(frame):
        for i, line in enumerate(lines):
            x = list(range(frame+1))
            y = [step[i] if i < len(step) else None
                 for step in steps[:frame+1]]
            # Filter out None values for frames not yet filled
            y_clean = [val for val in y if val is not None]
            x_clean = x[-len(y_clean):]
            line.set_data(x_clean, y_clean)
        return lines

    ani = animation.FuncAnimation(
        fig, update, frames=len(steps),
        init_func=init, blit=True, interval=500, repeat=False
    )
    plt.show()