import tkinter as tk
from tkinter import messagebox
from algorithms import simulate_fifo, simulate_lru, simulate_optimal
from utils import plot_individual_graph

def individual_mode():
    """Launch Individual Mode GUI."""
    def start_simulation():
        algorithm = combo_algorithm.get()
        pages_str = entry_pages.get()
        frames_str = entry_frames.get()
        pages, frames = validate_input(pages_str, frames_str)

        if not algorithm:
            messagebox.showerror("Input Error", "Please select an algorithm.")
            return

        if pages is None or frames is None:
            return

        if algorithm == "FIFO":
            steps, faults = simulate_fifo(pages, frames)
            plot_individual_graph(steps, faults, title=f"{algorithm} Mode")
        elif algorithm == "LRU":
            steps, faults = simulate_lru(pages, frames)
            plot_individual_graph(steps, faults, title=f"{algorithm} Mode")
        elif algorithm == "Optimal":
            steps, faults = simulate_optimal(pages, frames)
            plot_individual_graph(steps, faults, title=f"{algorithm} Mode")

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
    root.title("Page Replacement Algorithms - Individual Mode")

    tk.Label(root, text="Select Algorithm:").pack(pady=10)
    combo_algorithm = tk.StringVar()
    combo_algorithm.set("FIFO")
    tk.OptionMenu(root, combo_algorithm, "FIFO", "LRU", "Optimal").pack(pady=10)

    tk.Label(root, text="Enter page numbers (space-separated):").pack(pady=10)
    entry_pages = tk.Entry(root, font=("Arial", 14))
    entry_pages.pack(pady=10)

    tk.Label(root, text="Enter number of frames:").pack(pady=10)
    entry_frames = tk.Entry(root, font=("Arial", 14))
    entry_frames.pack(pady=10)

    start_button = tk.Button(root, text="Start Simulation", font=("Arial", 14), command=start_simulation)
    start_button.pack(pady=20)

    root.mainloop()
