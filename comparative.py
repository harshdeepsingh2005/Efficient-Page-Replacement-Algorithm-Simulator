import tkinter as tk
from tkinter import messagebox
from algorithms import simulate_fifo, simulate_lru, simulate_optimal
from utils import plot_comparative_graph

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

        plot_comparative_graph(
            fifo_steps, lru_steps, optimal_steps, fifo_faults, lru_faults, optimal_faults, title="Comparative Mode"
        )

    def validate_input(pages_str, frames_str):
        try:
            pages = [int(x) for x in pages_str.split()]
            frames = int(frames_str)
            if frames <= 0:
                raise ValueError
            return pages, frames
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please enter valid pages and frames.")
            return None, None

    # GUI setup
    root = tk.Tk()
    root.title("Page Replacement Algorithms - Comparative Mode")

    tk.Label(root, text="Enter page numbers (space-separated):").pack(pady=10)
    entry_pages = tk.Entry(root, font=("Arial", 14))
    entry_pages.pack(pady=10)

    tk.Label(root, text="Enter number of frames:").pack(pady=10)
    entry_frames = tk.Entry(root, font=("Arial", 14))
    entry_frames.pack(pady=10)

    start_button = tk.Button(root, text="Start Simulation", font=("Arial", 14), command=start_simulation)
    start_button.pack(pady=20)

    root.mainloop()
