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
  <li><strong>{{ r.class_date | date: "%b %-d" }}</strong>{% if r.lecture_no %} &middot; L{{ r.lecture_no }}{% endif %} &middot; <a href="{{ r.url | relative_url }}">{{ r.title | remove: "Readings & resources: " }}</a></li>
{%- endfor %}
</ul>
{% else %}
_Coming soon._
{% endif %}

## Tools & references

_Coming soon._

## Datasets

_Coming soon._
