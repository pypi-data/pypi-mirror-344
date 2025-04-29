# tests/test_scoring.py
import pytest
from prival.scoring import compute_overall_score

def test_compute_overall_score_empty():
    assert compute_overall_score({}, {}) == 0.0

def test_compute_overall_score_simple():
    scores = {'a': 1.0, 'b': 0.5}
    weights = {'a': 0.5, 'b': 0.5}
    assert compute_overall_score(scores, weights) == 0.75