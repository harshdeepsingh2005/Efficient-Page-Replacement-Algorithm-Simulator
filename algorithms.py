def simulate_fifo(pages, frames):
    """Simulate FIFO page replacement algorithm."""
    frames_list = [-1] * frames
    page_faults = 0
    steps = []
    
    for page in pages:
        if page not in frames_list:
            page_faults += 1
            frames_list = frames_list[1:] + [page]
        steps.append(list(frames_list))  # Capture the state of the frames at each step
    
    return steps, page_faults

def simulate_lru(pages, frames):
    """Simulate LRU page replacement algorithm."""
    frames_list = []
    page_faults = 0
    steps = []
    
    for page in pages:
        if page not in frames_list:
            page_faults += 1
            if len(frames_list) >= frames:
                frames_list.pop(0)
            frames_list.append(page)
        else:
            frames_list.remove(page)
            frames_list.append(page)
        steps.append(list(frames_list))  # Capture the state of the frames at each step
    
    return steps, page_faults

def simulate_optimal(pages, frames):
    """Simulate Optimal Page Replacement."""
    frame = []
    page_faults = 0
    steps = []

    for i in range(len(pages)):
        if pages[i] not in frame:
            if len(frame) < frames:
                frame.append(pages[i])
            else:
                # Find the page to replace (the one that is used furthest in the future)
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
        
        # Append a copy of the current frame, ensuring that no 'invalid' entries are added
        steps.append(frame[:])

    return steps, page_faults
