"""
algorithm.py
------------
This module contains the core logic for FIFO, LRU, and Optimal page replacement algorithms.
"""

def simulate_fifo(pages, frames):
    """Simulate FIFO Page Replacement."""
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
    """Simulate LRU Page Replacement."""
    frame = []
    page_faults = 0
    steps = []
    page_usage = []

    for page in pages:
        if page not in frame:
            if len(frame) < frames:
                frame.append(page)
                page_usage.append(page)
            else:
                lru_page = page_usage[0]
                frame[frame.index(lru_page)] = page
                page_usage.remove(lru_page)
                page_usage.append(page)
            page_faults += 1
        else:
            page_usage.remove(page)
            page_usage.append(page)
        steps.append(frame[:])
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
