def extract_root_causes(graph, top_k=3):
    """
    Extracts the multi-root causality from the graph.
    Returns the top K processes or metrics that have the highest influence score.
    """
    # Filter only PROCESS nodes that have influenced something
    candidates = [n for n in graph.nodes.values() if n.type == "PROCESS" and n.influence_score > 0]
    
    # Sort by influence
    candidates.sort(key=lambda x: x.influence_score, reverse=True)
    
    # If no processes found causing issues, look at general metrics
    if not candidates:
        metrics = [n for n in graph.nodes.values() if n.type == "METRIC" and n.influence_score > 0]
        metrics.sort(key=lambda x: x.influence_score, reverse=True)
        return [{"cause": m.id, "score": m.influence_score} for m in metrics[:top_k]]
        
    return [{"cause": c.id.replace("PROC_", ""), "score": c.influence_score} for c in candidates[:top_k]]
