---
layout: about
title: Home
permalink: /
hide_default_header: true
news: true
latest_posts: false
selected_papers: true
social: true
---

<section class="lab-hero">
  <div class="lab-hero__inner">
    <p class="lab-hero__eyebrow">Srivastava Lab &middot; The Wistar Institute &middot; Philadelphia</p>
    <h1 class="lab-hero__title">
      Computational tools<br>
      for <span class="lab-hero__accent">understanding</span><br>
      <span class="lab-hero__accent">how cells decide</span>.
    </h1>
    <p class="lab-hero__lead">
      We build probabilistic models and high-performance algorithms
      that translate multimodal single-cell measurements into
      a precise, uncertainty-aware picture of gene regulation and cell fate.
    </p>
    <div class="lab-hero__cta">
      <a class="lab-btn lab-btn--primary" href="{{ 'research' | relative_url }}">Our research &rarr;</a>
      <a class="lab-btn lab-btn--ghost" href="{{ 'publications' | relative_url }}">Publications</a>
      <a class="lab-btn lab-btn--ghost" href="{{ 'people' | relative_url }}">People</a>
    </div>
  </div>
</section>

We are a computational biology group developing methods at the intersection
of **statistical machine learning**, **single-cell genomics**, and
**chromatin biology**. Our tools — from the
[salmon](https://salmon.readthedocs.io) / [alevin](https://github.com/COMBINE-lab/alevin-fry)
quantification ecosystem to
[Signac](https://stuartlab.org/signac/) and
[scCUT&Tag-pro](https://www.nature.com/articles/s41587-022-01250-0) —
are used by thousands of labs worldwide.
Our biology questions center on the regulatory logic that drives cell
differentiation, and how that logic breaks down in disease.

---

<section class="lab-section">
  <h2 class="lab-section__title">Research themes</h2>
  <p class="lab-section__sub">Four interlocking threads — from fast algorithms to chromatin biology — with a bias for tools other labs can use the next morning.</p>
  <div class="lab-grid">
    <a class="lab-card" href="{{ 'research' | relative_url }}#multimodal-single-cell">
      <span class="lab-card__icon">🧬</span>
      <h3 class="lab-card__title">Multimodal single-cell</h3>
      <p class="lab-card__text">Joint models for RNA, chromatin, histone marks, and surface proteins — one cell, one coherent state.</p>
    </a>
    <a class="lab-card" href="{{ 'research' | relative_url }}#uncertainty-aware-ml">
      <span class="lab-card__icon">📐</span>
      <h3 class="lab-card__title">Uncertainty-aware ML</h3>
      <p class="lab-card__text">Bayesian and probabilistic methods that propagate what we don&rsquo;t know all the way through the analysis.</p>
    </a>
    <a class="lab-card" href="{{ 'research' | relative_url }}#scalable-quantification">
      <span class="lab-card__icon">⚡</span>
      <h3 class="lab-card__title">Scalable quantification</h3>
      <p class="lab-card__text">Memory-frugal algorithms (salmon &middot; alevin &middot; alevin-fry) that make atlas-scale analysis practical.</p>
    </a>
    <a class="lab-card" href="{{ 'research' | relative_url }}#regulatory-genomics">
      <span class="lab-card__icon">🧠</span>
      <h3 class="lab-card__title">Regulatory genomics</h3>
      <p class="lab-card__text">Chromatin dynamics and gene-regulatory networks across differentiation and disease.</p>
    </a>
  </div>
</section>

<section class="lab-section">
  <h2 class="lab-section__title">Featured tools &amp; papers</h2>
  <p class="lab-section__sub">Open-source by default — software ships alongside every method.</p>
  <div class="lab-pubstrip">
    <a class="lab-pubstrip__item" href="https://www.nature.com/articles/s41592-022-01408-3" title="alevin-fry — Nature Methods 2022">
      <img src="{{ '/assets/img/publication_preview/fry.jpg' | relative_url }}" alt="alevin-fry">
      <span>alevin-fry</span>
    </a>
    <a class="lab-pubstrip__item" href="https://www.nature.com/articles/s41587-022-01250-0" title="scCUT&Tag-pro — Nature Biotechnology 2022">
      <img src="{{ '/assets/img/publication_preview/cnt.jpg' | relative_url }}" alt="scCUT&Tag-pro">
      <span>scCUT&amp;Tag-pro</span>
    </a>
    <a class="lab-pubstrip__item" href="https://www.nature.com/articles/s41592-021-01282-5" title="Signac — Nature Methods 2021">
      <img src="{{ '/assets/img/publication_preview/signac.jpg' | relative_url }}" alt="Signac">
      <span>Signac</span>
    </a>
    <a class="lab-pubstrip__item" href="https://www.nature.com/articles/s41587-023-01767-y" title="Seurat v5 — Nature Biotechnology 2023">
      <img src="{{ '/assets/img/publication_preview/sv5.jpg' | relative_url }}" alt="Seurat v5">
      <span>Seurat&nbsp;v5</span>
    </a>
    <a class="lab-pubstrip__item" href="https://link.springer.com/article/10.1186/s13059-019-1670-y" title="alevin — Genome Biology 2019">
      <img src="{{ '/assets/img/publication_preview/alevin.jpg' | relative_url }}" alt="alevin">
      <span>alevin</span>
    </a>
    <a class="lab-pubstrip__item" href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02151-8" title="Alignment &amp; mapping — Genome Biology 2020">
      <img src="{{ '/assets/img/publication_preview/aln.jpg' | relative_url }}" alt="Alignment study">
      <span>aln&nbsp;study</span>
    </a>
  </div>
</section>
