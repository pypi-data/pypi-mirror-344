import os
import yaml

from .detectors import (
    clarity,
    ambiguity,
    step_guidance,
    verbosity,
    injection_risk,
    context_completeness,
    ethic_compliance,
    structural_cleanness,
    relevance,
    feasibility,
    grammar_spelling,
    length_appropriateness,
    diversity,
)
from .scoring import aggregate_scores

# Mapping from dimension name to detector function
_DETECTORS = {
    'clarity': clarity.detect_clarity,
    'ambiguity': ambiguity.detect_ambiguity,
    'step_guidance': step_guidance.detect_step_guidance,
    'verbosity': verbosity.detect_verbosity,
    'injection_risk': injection_risk.detect_injection_risk,
    'context_completeness': context_completeness.detect_context_completeness,
    'ethic_compliance': ethic_compliance.detect_ethic_compliance,
    'structural_cleanness': structural_cleanness.structural_cleanness,
    'relevance': relevance.detect_relevance,
    'feasibility': feasibility.detect_feasibility,
    'grammar_spelling': grammar_spelling.grammar_spelling,
    'length_appropriateness': length_appropriateness.detect_length_appropriateness,
    'diversity': diversity.detect_diversity,
}

def evaluate_prompt(prompt: str) -> dict:
    """
    Evaluate the given prompt across all enabled dimensions and return
    a dictionary of results plus a total score.
    """
    # Load configuration
    here = os.path.dirname(__file__)
    config_path = os.path.abspath(os.path.join(here, os.pardir, 'config.yaml'))
    with open(config_path, encoding='utf-8') as cfg_file:
        config = yaml.safe_load(cfg_file)

    enabled = config.get('enabled_dimensions', [])
    results = {}
    for dim, func in _DETECTORS.items():
        if dim in enabled:
            try:
                results[dim] = func(prompt)
            except Exception as e:
                results[dim] = {'score': None, 'suggestions': [f'Error in {dim}: {e}']}

    # Compute total score
    total = aggregate_scores(results, config)
    results['total_score'] = total
    return results
