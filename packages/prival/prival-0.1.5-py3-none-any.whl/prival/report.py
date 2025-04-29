# report.py
"""
生成 HTML 与 Markdown 格式的报告，包含各维度得分和建议。
"""

from jinja2 import Template

HTML_TEMPLATE = """
<html>
<head><title>PRIVAL Prompt 验证报告</title></head>
<body>
<h2>PRIVAL 验证报告</h2>
<p>Overall Score: {{ overall }}</p>
<table border=1 cellpadding=5>
  <tr><th>维度</th><th>分数</th><th>建议</th></tr>
  {% for dim, score in scores.items() %}
  <tr>
    <td>{{ dim }}</td>
    <td>{{ score }}</td>
    <td>{{ suggestions[dim] | join('; ') }}</td>
  </tr>
  {% endfor %}
</table>
</body>
</html>
"""

MD_TEMPLATE = """
# PRIVAL Prompt 验证报告

**Overall Score:** {{ overall }}

| 维度 | 分数 | 建议 |
|-----|-----|------|
{% for dim, score in scores.items() %}
| {{ dim }} | {{ score }} | {{ suggestions[dim] | join('; ') }} |
{% endfor %}
"""

def generate_html_report(data: dict) -> str:
    """返回 HTML 格式报告字符串。"""
    tmpl = Template(HTML_TEMPLATE)
    return tmpl.render(scores=data['scores'], suggestions=data['suggestions'], overall=data['overall'])


def generate_md_report(data: dict) -> str:
    """返回 Markdown 格式报告字符串。"""
    tmpl = Template(MD_TEMPLATE)
    return tmpl.render(scores=data['scores'], suggestions=data['suggestions'], overall=data['overall'])