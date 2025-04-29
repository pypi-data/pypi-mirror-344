# tests/test_report.py
import pytest
from prival.report import generate_md_report, generate_html_report

def test_generate_reports():
    data = {
        'scores': {'clarity': 0.8},
        'suggestions': {'clarity': ['Be more specific']},
        'overall': 0.8
    }
    md = generate_md_report(data)
    assert 'clarity' in md and 'Be more specific' in md
    html = generate_html_report(data)
    assert '<td>clarity</td>' in html