import copy

def first_fit(blocks_input, processes):
    """
    First Fit: Allocate the first hole that is big enough.
    """
    # Har block mein 'p_list' add ki hai jo multiple processes ka record rakhegi
    blocks = [{"id": i, "size": s, "remaining": s, "p_list": []} for i, s in enumerate(blocks_input)]
    history = []
    allocation = [-1] * len(processes)

    for i, p_size in enumerate(processes):
        for b in blocks:
            if b["remaining"] >= p_size:
                # 1. Process ka record block ki p_list mein daalo
                b["p_list"].append({
                    "name": f"P{i+1}",
                    "size": p_size
                })
                # 2. Remaining space minus karo
                b["remaining"] -= p_size
                allocation[i] = b["id"]
                break
        history.append(copy.deepcopy(blocks))
    
    return history, allocation

def best_fit(blocks_input, processes):
    """
    Best Fit: Allocate the smallest hole that is big enough.
    """
    blocks = [{"id": i, "size": s, "remaining": s, "p_list": []} for i, s in enumerate(blocks_input)]
    history = []
    allocation = [-1] * len(processes)

    for i, p_size in enumerate(processes):
        best_idx = -1
        for j, b in enumerate(blocks):
            if b["remaining"] >= p_size:
                if best_idx == -1 or b["remaining"] < blocks[best_idx]["remaining"]:
                    best_idx = j
        
        if best_idx != -1:
            # Process ka record best block ki p_list mein daalo
            blocks[best_idx]["p_list"].append({
                "name": f"P{i+1}",
                "size": p_size
            })
            blocks[best_idx]["remaining"] -= p_size
            allocation[i] = blocks[best_idx]["id"]
            
        history.append(copy.deepcopy(blocks))
    
    return history, allocation

def worst_fit(blocks_input, processes):
    """
    Worst Fit: Allocate the largest hole available.
    """
    blocks = [{"id": i, "size": s, "remaining": s, "p_list": []} for i, s in enumerate(blocks_input)]
    history = []
    allocation = [-1] * len(processes)

    for i, p_size in enumerate(processes):
        worst_idx = -1
        for j, b in enumerate(blocks):
            if b["remaining"] >= p_size:
                if worst_idx == -1 or b["remaining"] > blocks[worst_idx]["remaining"]:
                    worst_idx = j
        
        if worst_idx != -1:
            # Process ka record worst block ki p_list mein daalo
            blocks[worst_idx]["p_list"].append({
                "name": f"P{i+1}",
                "size": p_size
            })
            blocks[worst_idx]["remaining"] -= p_size
            allocation[i] = blocks[worst_idx]["id"]
            
        history.append(copy.deepcopy(blocks))
    
    return history, allocation

def next_fit(blocks_input, processes):
    """
    Next Fit: Starts searching from the last allocation point.
    """
    blocks = [{"id": i, "size": s, "remaining": s, "p_list": []} for i, s in enumerate(blocks_input)]
    history = []
    allocation = [-1] * len(processes)
    last_idx = 0
    n = len(blocks)

    for i, p_size in enumerate(processes):
        for j in range(n):
            current = (last_idx + j) % n
            if blocks[current]["remaining"] >= p_size:
                # Process ka record current block ki p_list mein daalo
                blocks[current]["p_list"].append({
                    "name": f"P{i+1}",
                    "size": p_size
                })
                blocks[current]["remaining"] -= p_size
                allocation[i] = blocks[current]["id"]
                last_idx = current 
                break
        
        history.append(copy.deepcopy(blocks))
    
    return history, allocation