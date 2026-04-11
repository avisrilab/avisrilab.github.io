---
layout: page
title: People
description: The humans behind the code and the experiments.
permalink: /people/
nav: true
nav_order: 3
published: true
role_order:
  - Principal Investigator
  - Postdoctoral Researchers
  - Graduate Students
  - Research Assistants
  - Undergraduate Researchers
  - Visiting Scientists
  - Alumni
---

The lab brings together computer scientists, statisticians, and biologists.
We come from different training backgrounds and pull on each other&rsquo;s
expertise to ask sharper questions and build better tools.

{% comment %}
  Render members grouped by `role`. Roles are listed in `page.role_order`
  above; any member whose role is not in that list still renders, in a
  trailing block. New members are added by dropping a photo + running
  `bin/add_member.py` (see the README in `bin/`).
{% endcomment %}

{%- assign all_members = site.people | sort: "importance" -%}
{%- assign rendered_roles = "" | split: "," -%}

{%- for role in page.role_order -%}
  {%- assign members_in_role = all_members | where: "role", role -%}
  {%- if members_in_role.size > 0 %}
<section class="lab-role-block">
  <h2 class="lab-role-block__title">{{ role }}</h2>
  <div class="lab-people-grid">
    {%- for member in members_in_role %}
    <a class="lab-member" href="{{ member.url | relative_url }}">
      {%- if member.img %}
      <img class="lab-member__photo" src="{{ member.img | relative_url }}" alt="{{ member.title }}">
      {%- endif %}
      <p class="lab-member__name">{{ member.title }}</p>
      {%- if member.tagline %}
      <p class="lab-member__role">{{ member.tagline }}</p>
      {%- elsif member.description %}
      <p class="lab-member__role">{{ member.description | strip_html | truncate: 80 }}</p>
      {%- endif %}
    </a>
    {%- endfor %}
  </div>
</section>
    {%- assign rendered_roles = rendered_roles | push: role -%}
  {%- endif -%}
{%- endfor -%}

{%- assign other_members = "" | split: "," -%}
{%- for member in all_members -%}
  {%- unless rendered_roles contains member.role -%}
    {%- assign other_members = other_members | push: member -%}
  {%- endunless -%}
{%- endfor -%}

{%- if other_members.size > 0 %}
<section class="lab-role-block">
  <h2 class="lab-role-block__title">Lab members</h2>
  <div class="lab-people-grid">
    {%- for member in other_members %}
    <a class="lab-member" href="{{ member.url | relative_url }}">
      {%- if member.img %}
      <img class="lab-member__photo" src="{{ member.img | relative_url }}" alt="{{ member.title }}">
      {%- endif %}
      <p class="lab-member__name">{{ member.title }}</p>
      {%- if member.tagline %}
      <p class="lab-member__role">{{ member.tagline }}</p>
      {%- endif %}
    </a>
    {%- endfor %}
  </div>
</section>
{%- endif %}
