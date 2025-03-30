import tkinter as tk
from tkinter import ttk, messagebox
from algorithms import simulate_fifo, simulate_lru, simulate_optimal
from utils import validate_input, plot_individual_graph

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
        elif algorithm == "LRU":
            steps, faults = simulate_lru(pages, frames)
        elif algorithm == "Optimal":
            steps, faults = simulate_optimal(pages, frames)
        plot_individual_graph(pages,steps, faults, pages)
    # GUI setup
    root = tk.Tk()
    root.title("Individual Mode")
    root.geometry("400x300")

    label_pages = tk.Label(root, text="Enter Pages (space-separated):", font=("Arial", 12))
    label_pages.pack(pady=10)
    entry_pages = tk.Entry(root, font=("Arial", 12))
    entry_pages.pack(pady=10)

    label_frames = tk.Label(root, text="Enter Number of Frames:", font=("Arial", 12))
    label_frames.pack(pady=10)
    entry_frames = tk.Entry(root, font=("Arial", 12))
    entry_frames.pack(pady=10)

    label_algo = tk.Label(root, text="Select Algorithm:", font=("Arial", 12))
    label_algo.pack(pady=10)
    combo_algorithm = ttk.Combobox(root, values=["FIFO", "LRU", "Optimal"], font=("Arial", 12))
    combo_algorithm.pack(pady=10)

    btn_simulate = tk.Button(root, text="Simulate", font=("Arial", 12), command=start_simulation)
    btn_simulate.pack(pady=20)

    root.mainloop()
