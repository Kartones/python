# {{ SITENAME }} - Archives with descriptions

## Articles

{% for article in articles %}
- [{{ article.title }}]({{ SITEURL }}/{{ article.url }}index.html.md) - {{ article.date.strftime("%Y-%m-%d") }}
  Summary: {{ article.description }}
{% endfor %}

## Pages

{% for page in pages + hidden_pages + draft_pages if page.slug not in LLMS_EXPORT_CONTENT_EXCLUSIONS %}
- [{{ page.title }}]({{ SITEURL }}/{{ page.url }}index.html.md)
  Summary: {{ page.description }}
{% endfor %}
