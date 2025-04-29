"""
Scoring utilities for PRIVAL.
Aggregates individual dimension scores into a total score.
"""

def aggregate_scores(results: dict, config: dict) -> float:
    """
    Compute the overall score as the simple average of available numeric scores.
    """
    scores = []
    for dim, res in results.items():
        score = res.get('score')
        if isinstance(score, (int, float)):
            scores.append(score)
    if not scores:
        return None
    return sum(scores) / len(scores)
