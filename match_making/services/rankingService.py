

def ranking(candidates):
    # candidates: [(UserBase instances, similarity), ...]
    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    return sorted_candidates[:10]