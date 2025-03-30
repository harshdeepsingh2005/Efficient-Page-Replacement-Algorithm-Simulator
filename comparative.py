import tkinter as tk
from algorithms import simulate_fifo, simulate_lru, simulate_optimal
from utils import validate_input, plot_comparative_graph

def comparative_mode():
    """Launch Comparative Mode GUI."""
    def start_simulation():
        pages_str = entry_pages.get()
        frames_str = entry_frames.get()
        pages, frames = validate_input(pages_str, frames_str)

        if pages is None or frames is None:
            return

        fifo_steps, fifo_faults = simulate_fifo(pages, frames)
        lru_steps, lru_faults = simulate_lru(pages, frames)
        optimal_steps, optimal_faults = simulate_optimal(pages, frames)

        plot_comparative_graph(pages,
            fifo_steps, lru_steps, optimal_steps, fifo_faults, lru_faults, optimal_faults, title="Comparative Mode"
        )

    # GUI setup
    root = tk.Tk()
    root.title("Comparative Mode")
    root.geometry("400x250")

    label_pages = tk.Label(root, text="Enter Pages (space-separated):", font=("Arial", 12))
    label_pages.pack(pady=10)
    entry_pages = tk.Entry(root, font=("Arial", 12))
    entry_pages.pack(pady=10)

    label_frames = tk.Label(root, text="Enter Number of Frames:", font=("Arial", 12))
    label_frames.pack(pady=10)
    entry_frames = tk.Entry(root, font=("Arial", 12))
    entry_frames.pack(pady=10)

    btn_simulate = tk.Button(root, text="Simulate", font=("Arial", 12), command=start_simulation)
    btn_simulate.pack(pady=20)

    root.mainloop()
