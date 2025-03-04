import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def fifo(page_refs, num_frames):
    page_faults = 0
    frames = []
    fault_history = []

    for page in page_refs:
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
        fault_history.append(list(frames))

    return page_faults, fault_history

def lru(page_refs, num_frames):
    page_faults = 0
    frames = []
    recent_usage = []
    fault_history = []

    for page in page_refs:
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                lru_page = recent_usage.pop(0)
                frames.remove(lru_page)
                frames.append(page)
        else:
            recent_usage.remove(page)
        recent_usage.append(page)
        fault_history.append(list(frames))

    return page_faults, fault_history

def optimal(page_refs, num_frames):
    page_faults = 0
    frames = []
    fault_history = []

    for i in range(len(page_refs)):
        page = page_refs[i]
        if page not in frames:
            page_faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                future_use = {frame: float('inf') for frame in frames}
                for j in range(i + 1, len(page_refs)):
                    if page_refs[j] in frames and future_use[page_refs[j]] == float('inf'):
                        future_use[page_refs[j]] = j
                victim = max(frames, key=lambda x: future_use[x])
                frames.remove(victim)
                frames.append(page)
        fault_history.append(list(frames))

    return page_faults, fault_history

def animate_results(page_refs, fault_history, algorithm_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, len(page_refs))
    ax.set_ylim(min(page_refs) - 1, max(page_refs) + 1)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Page Numbers")
    ax.set_title(f"{algorithm_name} Page Replacement Animation")
    ax.grid(True)
    
    lines = [ax.plot([], [], marker='o', linestyle='-', label=f"Frame {i+1}")[0] for i in range(len(fault_history[0]))]
    
    def update(frame_idx):
        for i, line in enumerate(lines):
            if i < len(fault_history[frame_idx]):
                line.set_data(range(frame_idx + 1), [fault_history[j][i] for j in range(frame_idx + 1)])
        return lines
    
    ani = animation.FuncAnimation(fig, update, frames=len(page_refs), interval=300, repeat=False)
    plt.legend()
    plt.show()

def simulate_algorithm(page_refs, num_frames, algorithm):
    if algorithm == "FIFO":
        faults, history = fifo(page_refs, num_frames)
    elif algorithm == "LRU":
        faults, history = lru(page_refs, num_frames)
    elif algorithm == "Optimal":
        faults, history = optimal(page_refs, num_frames)
    else:
        messagebox.showerror("Error", "Invalid Algorithm Selected")
        return

    result = f"Algorithm: {algorithm}\nPage Faults: {faults}\n\nFrame History:\n"
    for step, frame in enumerate(history):
        result += f"Step {step + 1}: {frame}\n"

    messagebox.showinfo("Simulation Results", result)
    animate_results(page_refs, history, algorithm)

def start_simulation():
    try:
        page_refs = list(map(int, entry_page_refs.get().split()))
        num_frames = int(entry_num_frames.get())
        algorithm = algo_var.get()
        if not algorithm:
            raise ValueError("No Algorithm Selected")
        simulate_algorithm(page_refs, num_frames, algorithm)
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

# GUI Setup
root = tk.Tk()
root.title("Page Replacement Algorithm Simulator")
root.geometry("600x400")  # Wider window

# Apply dark theme using custom ttk style
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#333333", foreground="#FFFFFF", font=("Arial", 12))
style.configure("TEntry", fieldbackground="#555555", foreground="#FFFFFF", font=("Arial", 12))
style.configure("TRadiobutton", background="#333333", foreground="#FFFFFF", font=("Arial", 12))
style.configure("TButton", background="#555555", foreground="#FFFFFF", font=("Arial", 12))
style.configure("TFrame", background="#333333")

# Main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Input Fields
ttk.Label(main_frame, text="Page Reference Sequence (space-separated):").pack(pady=5)
entry_page_refs = ttk.Entry(main_frame, width=50)
entry_page_refs.pack(pady=5)

ttk.Label(main_frame, text="Number of Frames:").pack(pady=5)
entry_num_frames = ttk.Entry(main_frame, width=20)
entry_num_frames.pack(pady=5)

ttk.Label(main_frame, text="Select Algorithm:").pack(pady=10)
algo_var = tk.StringVar(value="")
ttk.Radiobutton(main_frame, text="FIFO", variable=algo_var, value="FIFO").pack()
ttk.Radiobutton(main_frame, text="LRU", variable=algo_var, value="LRU").pack()
ttk.Radiobutton(main_frame, text="Optimal", variable=algo_var, value="Optimal").pack()

# Start Button
ttk.Button(main_frame, text="Start Simulation", command=start_simulation).pack(pady=20)

# Run the GUI
root.mainloop()
