import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to simulate algorithms
def simulate_fifo(pages, frames):
    frame = []
    page_faults = 0
    steps = []

    for page in pages:
        if page not in frame:
            if len(frame) < frames:
                frame.append(page)
            else:
                frame.pop(0)
                frame.append(page)
            page_faults += 1
        steps.append(frame[:])

    return steps, page_faults

def simulate_lru(pages, frames):
    frame = []
    page_faults = 0
    steps = []

    for page in pages:
        if page not in frame:
            if len(frame) < frames:
                frame.append(page)
            else:
                frame.pop(0)
                frame.append(page)
            page_faults += 1
        else:
            frame.remove(page)
            frame.append(page)
        steps.append(frame[:])

    return steps, page_faults

def simulate_optimal(pages, frames):
    frame = []
    page_faults = 0
    steps = []

    for i in range(len(pages)):
        if pages[i] not in frame:
            if len(frame) < frames:
                frame.append(pages[i])
            else:
                future = pages[i + 1:]
                farthest = -1
                index = -1
                for j in range(len(frame)):
                    if frame[j] not in future:
                        index = j
                        break
                    else:
                        pos = future.index(frame[j])
                        if pos > farthest:
                            farthest = pos
                            index = j
                frame[index] = pages[i]
            page_faults += 1
        steps.append(frame[:])

    return steps, page_faults
def validate_input(pages_str, frames_str):
    try:
        pages = list(map(int, pages_str.split()))
        frames = int(frames_str)
        if frames <= 0:
            raise ValueError("Number of frames must be positive.")
        return pages, frames
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")
        return None, None

# Popup to show steps and graph together with animation
def show_steps_and_graph(title, steps, algorithm, page_faults):
    step_window = tk.Toplevel(root)
    step_window.title(title)
    step_window.geometry("900x600")

    # Frame for steps
    steps_frame = tk.Frame(step_window)
    steps_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_display = tk.Label(steps_frame, text="", font=("Helvetica", 16))
    frame_display.pack(expand=True, pady=20)

    # Frame for graph
    graph_frame = tk.Frame(step_window)
    graph_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    fig, ax = plt.subplots()
    ax.set_title(f"{algorithm} - Page Faults: {page_faults}")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Pages in Frame")

    x_data, y_data = [], []
    line, = ax.plot([], [], marker="o", color="cyan")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

    def init():
        ax.set_xlim(1, len(steps))
        ax.set_ylim(0, max(len(frame) for frame in steps) + 1)
        return line,

    current_step = [0]

    def update(frame):
        if current_step[0] < len(steps):
            frame_display.config(text=f"Step {current_step[0] + 1}: {steps[current_step[0]]}")
            x_data.append(current_step[0] + 1)
            y_data.append(len(steps[current_step[0]]))
            line.set_data(x_data, y_data)
            current_step[0] += 1
        return line,

    def pause_continue():
        #Toggle between Pause and Continue
        nonlocal is_paused
        if is_paused:
            ani.event_source.start()  #Continue the animation
            btn_pause_continue.config(text="Pause")  # Change button text to "Pause"
        else:
            ani.event_source.stop()  # Pause the animation
            btn_pause_continue.config(text="Continue")  # Change button text to "Continue"
        is_paused = not is_paused  # Toggle the state

    is_paused = False  #Track if the animation is paused

    ani = animation.FuncAnimation(fig, update, frames=len(steps), init_func=init, blit=False, interval=1200)
    button_frame = tk.Frame(step_window)  # Create a frame for the buttons
    button_frame.pack(side="top", fill="x", pady=10)

    #Pause/Continue Button (same button toggling between Pause and Continue)
    btn_pause_continue = tk.Button(button_frame, text="Pause", command=pause_continue, font=("Arial", 12))
    btn_pause_continue.pack(side="bottom", padx=5)

    def move_back():
        nonlocal current_step
        if current_step[0] > 0:
            current_step[0] -= 1  # Move one step back
            x_data.pop()  # Remove the last data point
            y_data.pop()
            line.set_data(x_data, y_data)  # Update the graph with new data
            frame_display.config(text=f"Step {current_step[0]}: {steps[current_step[0]]}")  # Update text
            canvas.draw()  # Redraw the graph
        # btn_pause_continue.config(text="Continue")  # Change button to "Continue" since it's stopped
        # is_paused = True

    btn_move_back = tk.Button(button_frame, text="Back", command=move_back, font=("Arial", 12))
    btn_move_back.pack(side="bottom", padx=5)

    canvas.draw()

# GUI Modes
def on_mode_selected(event):
    selected_mode = combo_mode.get()
    if selected_mode == "Individual":
        algorithm_selection_window("Individual")
    elif selected_mode == "Comparative":
        algorithm_selection_window("Comparative")

def algorithm_selection_window(mode):
    algo_window = tk.Toplevel(root)
    algo_window.title(f"{mode} Mode: Select Algorithm")
    algo_window.geometry("400x300")

    def simulate_selected_algorithm():
        algorithm = combo_algorithm.get()
        pages_str = entry_pages.get()
        frames_str = entry_frames.get()
        pages, frames = validate_input(pages_str, frames_str)

        if pages is None or frames is None:
            return

        if algorithm == "FIFO":
            steps, page_faults = simulate_fifo(pages, frames)
            show_steps_and_graph("FIFO Steps and Graph", steps, "FIFO", page_faults)
        elif algorithm == "LRU":
            steps, page_faults = simulate_lru(pages, frames)
            show_steps_and_graph("LRU Steps and Graph", steps, "LRU", page_faults)
        elif algorithm == "Optimal":
            steps, page_faults = simulate_optimal(pages, frames)
            show_steps_and_graph("Optimal Steps and Graph", steps, "Optimal", page_faults)
        elif mode == "Comparative":
            simulate_comparative_gui(pages, frames)

    label_algo = tk.Label(algo_window, text="Select Algorithm:", font=("Arial", 12))
    label_algo.pack(pady=10)

    combo_algorithm = ttk.Combobox(algo_window, values=["FIFO", "LRU", "Optimal"], font=("Arial", 12))
    combo_algorithm.pack(pady=5)

    btn_simulate = tk.Button(algo_window, text="Simulate", command=simulate_selected_algorithm, font=("Arial", 12))
    btn_simulate.pack(pady=20)

# Main GUI setup
root = tk.Tk()
root.title("Page Replacement Simulator")
root.geometry("800x600")

frame_main = tk.Frame(root, padx=20, pady=20)
frame_main.pack(fill="both", expand=True)

label_pages = tk.Label(frame_main, text="Enter Pages (space-separated):", font=("Arial", 12))
label_pages.grid(row=0, column=0, sticky="w", pady=5)

entry_pages = tk.Entry(frame_main, width=30, font=("Arial", 12))
entry_pages.grid(row=0, column=1, pady=5)

label_frames = tk.Label(frame_main, text="Enter Number of Frames:", font=("Arial", 12))
label_frames.grid(row=1, column=0, sticky="w", pady=5)

entry_frames = tk.Entry(frame_main, width=30, font=("Arial", 12))
entry_frames.grid(row=1, column=1, pady=5)

label_mode = tk.Label(frame_main, text="Select Mode:", font=("Arial", 12))
label_mode.grid(row=2, column=0, sticky="w", pady=5)

combo_mode = ttk.Combobox(frame_main, values=["Individual", "Comparative"], font=("Arial", 12))
combo_mode.grid(row=2, column=1, pady=5)
combo_mode.bind("<<ComboboxSelected>>", on_mode_selected)

root.mainloop()
