---
layout: default
title: "Readings & Resources"
nav_order: 2
---

# Readings & Resources

Readings and resources will be posted here as the semester progresses.

## By class meeting

{% assign by_class = site.readings | sort: "class_date" %}
{% if by_class.size > 0 %}
<ul>
{%- for r in by_class %}
  <li><strong>{% if r.class_no %}Day {{ r.class_no }}{% else %}{{ r.class_date | date: "%b %-d" }}{% endif %}</strong> ({{ r.class_date | date: "%b %-d" }}): <a href="{{ r.url | relative_url }}">{{ r.title | remove: "Readings & resources: " }}</a></li>
{%- endfor %}
</ul>
{% else %}
_Coming soon._
{% endif %}

## Tools & references

- Eisenstein, J. *[Natural Language Processing](https://github.com/jacobeisenstein/gt-nlp-class/blob/master/notes/eisenstein-nlp-notes.pdf)*. November 13, 2018.
- Schofield, X. "[tapi-text-data](https://github.com/xandaschofield/tapi-text-data/tree/main)." Text Analysis Pedagogy Institute 2022, Text Data Curation workshop.
- Blei, D. "[Probabilistic Topic Models](https://www.cs.columbia.edu/~blei/papers/Blei2012.pdf)." *Communications of the ACM* 55(4):77-84, 2012.
- Blei, D. "[Probabilistic Topic Models](https://yosinski.com/mlss12/media/slides/MLSS-2012-Blei-Probabilistic-Topic-Models.pdf)." MLSS 2012 slides.

## Datasets

_Coming soon._
