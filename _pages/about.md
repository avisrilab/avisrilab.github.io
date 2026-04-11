---
layout: about
title: Home
permalink: /
hide_default_header: true
news: true
latest_posts: false
selected_papers: false
social: true
---

<section class="lab-hero">
  <div class="lab-hero__inner">
    <p class="lab-hero__eyebrow">Srivastava Lab &middot; The Wistar Institute</p>
    <h1 class="lab-hero__title">
      Decoding cell fate with<br>
      <span class="lab-hero__accent">multimodal&nbsp;data</span> and
      <span class="lab-hero__accent">uncertainty&#8209;aware&nbsp;ML</span>.
    </h1>
    <p class="lab-hero__lead">
      We build computational tools and statistical models that turn raw single-cell and
      epigenomic measurements into a quantitative understanding of <em>how</em> the genome
      is read, regulated, and rewritten as cells make decisions.
    </p>
    <div class="lab-hero__cta">
      <a class="lab-btn lab-btn--primary" href="{{ 'research' | relative_url }}">Explore research &rarr;</a>
      <a class="lab-btn lab-btn--ghost" href="{{ 'publications' | relative_url }}">Publications</a>
      <a class="lab-btn lab-btn--ghost" href="{{ 'people' | relative_url }}">People</a>
    </div>
  </div>
</section>

<section class="lab-section">
  <h2 class="lab-section__title">What we work on</h2>
  <p class="lab-section__sub">
    Four interlocking threads that span methods, models, and biology &mdash; with a
    bias for tools other labs can use.
  </p>
  <div class="lab-grid">
    <a class="lab-card" href="{{ 'research' | relative_url }}#multimodal-single-cell">
      <span class="lab-card__icon">🧬</span>
      <h3 class="lab-card__title">Multimodal single-cell</h3>
      <p class="lab-card__text">
        Joint models for RNA, chromatin accessibility, histone marks, and surface
        proteins &mdash; so a single cell tells a single, coherent story.
      </p>
    </a>
    <a class="lab-card" href="{{ 'research' | relative_url }}#uncertainty-aware-ml">
      <span class="lab-card__icon">📐</span>
      <h3 class="lab-card__title">Uncertainty-aware ML</h3>
      <p class="lab-card__text">
        Bayesian and probabilistic methods that quantify what we don&rsquo;t know,
        not just what we predict. The error bars matter as much as the point estimates.
      </p>
    </a>
    <a class="lab-card" href="{{ 'research' | relative_url }}#scalable-quantification">
      <span class="lab-card__icon">⚡</span>
      <h3 class="lab-card__title">Scalable quantification</h3>
      <p class="lab-card__text">
        Fast, memory-frugal algorithms (the salmon &middot; alevin &middot; alevin-fry
        lineage) that make atlas-scale RNA-seq analysis practical on a laptop.
      </p>
    </a>
    <a class="lab-card" href="{{ 'research' | relative_url }}#regulatory-genomics">
      <span class="lab-card__icon">🧠</span>
      <h3 class="lab-card__title">Regulatory genomics</h3>
      <p class="lab-card__text">
        Linking chromatin state and gene-regulatory networks to the dynamics of
        differentiation, with applications across development and disease.
      </p>
    </a>
  </div>
</section>

<section class="lab-section">
  <h2 class="lab-section__title">Open-source, by default</h2>
  <p class="lab-section__sub">
    Our methods ship as community tools that other labs &mdash; experimental and computational &mdash; can pick up tomorrow.
  </p>
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
    <a class="lab-pubstrip__item" href="https://www.nature.com/articles/s41587-023-01767-y" title="Dictionary learning — Nature Biotechnology 2023">
      <img src="{{ '/assets/img/publication_preview/sv5.jpg' | relative_url }}" alt="Dictionary learning">
      <span>Seurat&nbsp;v5</span>
    </a>
    <a class="lab-pubstrip__item" href="https://link.springer.com/article/10.1186/s13059-019-1670-y" title="alevin — Genome Biology 2019">
      <img src="{{ '/assets/img/publication_preview/alevin.jpg' | relative_url }}" alt="alevin">
      <span>alevin</span>
    </a>
    <a class="lab-pubstrip__item" href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02151-8" title="Alignment & mapping methodology — Genome Biology 2020">
      <img src="{{ '/assets/img/publication_preview/aln.jpg' | relative_url }}" alt="Alignment methodology">
      <span>aln&nbsp;study</span>
    </a>
  </div>
</section>
