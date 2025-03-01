import matplotlib.pyplot as plt

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


def plot_results(page_refs, fault_history, algorithm_name):
    plt.figure(figsize=(10, 6))
    for i, frame in enumerate(zip(*fault_history)):
        plt.plot(range(len(page_refs)), frame, label=f"Frame {i + 1}")
    plt.scatter(range(len(page_refs)), page_refs, c='red', label="Page References")
    plt.xlabel("Steps")
    plt.ylabel("Page Numbers")
    plt.title(f"{algorithm_name} Page Replacement")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    print("Page Replacement Algorithm Simulator")
    page_refs = list(map(int, input("Enter page reference sequence (space-separated): ").split()))
    num_frames = int(input("Enter number of frames: "))
    print("\nSelect an algorithm:")
    print("1. FIFO")
    print("2. LRU")
    print("3. Optimal")
    choice = int(input("Enter choice (1/2/3): "))

    if choice == 1:
        faults, history = fifo(page_refs, num_frames)
        algo_name = "FIFO"
    elif choice == 2:
        faults, history = lru(page_refs, num_frames)
        algo_name = "LRU"
    elif choice == 3:
        faults, history = optimal(page_refs, num_frames)
        algo_name = "Optimal"
    else:
        print("Invalid choice!")
        return

    print(f"\nAlgorithm: {algo_name}")
    print(f"Page Faults: {faults}")
    print("Frame History:")
    for step, frame in enumerate(history):
        print(f"Step {step + 1}: {frame}")

    plot_results(page_refs, history, algo_name)


if __name__ == "__main__":
    main()
