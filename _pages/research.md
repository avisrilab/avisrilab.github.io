---
layout: page
title: Research
permalink: /research/
nav: true
nav_order: 1
published: true
---

The Srivastava Lab is a computational biology group. We design statistical
models, machine-learning methods, and high-performance algorithms that turn
modern genomics measurements &mdash; especially **multimodal single-cell**
data &mdash; into a quantitative picture of how the genome is read, regulated,
and rewritten as cells differentiate, respond to stimuli, and occasionally
go wrong.

Most of our work lives at the interface of three things:

1. *Methods* &mdash; principled, uncertainty-aware models of noisy biology;
2. *Tools* &mdash; fast, well-tested software that other labs actually run;
3. *Biology* &mdash; collaborations that take those tools all the way to a
   biological discovery.

We tend to ask the same question in many forms: *given a measurement of a
cell, what can we honestly say about its regulatory state, and with what
confidence?*

---

<div class="lab-research-theme" id="multimodal-single-cell">
<h3>1. Multimodal single-cell genomics</h3>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/scnt.png" -%}
    {% include figure.html path=profile_image_path class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix">
A single cell now routinely yields measurements of its transcriptome, its
chromatin accessibility, its histone modification landscape, and its surface
proteome &mdash; each modality with its own biases and blind spots. We build
joint models and integration frameworks that let those modalities reinforce
each other, so a single cell can be described by a single, coherent state
rather than a stack of disagreeing tables. This work powers community tools
like <a href="https://satijalab.org/seurat/">Seurat&nbsp;v5</a>,
<a href="https://stuartlab.org/signac/">Signac</a>, and
<a href="https://www.nature.com/articles/s41587-022-01250-0">scCUT&amp;Tag-pro</a>.
</div>
</article>
</div>

<div class="lab-research-theme" id="uncertainty-aware-ml">
<h3>2. Uncertainty-aware models for noisy biology</h3>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/bayesian.jpg" -%}
    {% include figure.html path=profile_image_path class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix">
Single-cell data is sparse, multi-mapping, and full of reads that quietly
disagree about which gene they came from. Most pipelines either discard the
ambiguity or hide it behind a confident-looking number. We instead build
Bayesian and probabilistic models that propagate that uncertainty all the
way through quantification, differential analysis, and downstream inference.
The result is methods like <a href="https://salmon.readthedocs.io/">alevin</a>
and <a href="https://github.com/COMBINE-lab/alevin-fry">alevin-fry</a>, plus
inferential-replicate workflows that let downstream analyses honour what we
genuinely <em>do not</em> know.
</div>
</article>
</div>

<div class="lab-research-theme" id="scalable-quantification">
<h3>3. Scalable, fast, and reproducible quantification</h3>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/salmon_logo.png" -%}
    {% include figure.html path=profile_image_path class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix">
Atlas-scale experiments are now the norm rather than the exception. We invest
heavily in algorithmic engineering &mdash; succinct indices, lightweight
mapping, careful UMI deduplication &mdash; to keep RNA-seq and single-cell
RNA-seq quantification fast, memory-frugal, and reproducible across machines.
This is the lineage that includes
<a href="https://academic.oup.com/bioinformatics/article/32/12/i192/2288985">RapMap</a>,
<a href="https://salmon.readthedocs.io/">salmon</a>, the
<a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02151-8">alignment-vs-mapping</a>
study, and the alevin/alevin-fry single-cell quantifiers. We care about
clean abstractions almost as much as benchmarks.
</div>
</article>
</div>

<div class="lab-research-theme" id="regulatory-genomics">
<h3>4. Chromatin dynamics and gene-regulatory networks</h3>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/cnt.jpg" -%}
    {% include figure.html path=profile_image_path class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix">
Chromatin state is the cell&rsquo;s working memory. We use single-cell
CUT&amp;Tag and related assays to track how regulatory elements switch on
and off across differentiation, and we build chromatin-aware gene-regulatory
network models that explicitly link those elements to their target genes.
The questions we love most are about <em>dynamics</em>: which regulators
move first, which downstream programs follow, and where the system becomes
brittle &mdash; with applications across normal development, immune
responses, and disease.
</div>
</article>
</div>

<div class="lab-research-theme" id="open-science">
<h3>5. Open science as a first-class deliverable</h3>
<div class="clearfix">
We treat <em>tools</em>, <em>tutorials</em>, and <em>benchmarks</em> as
research products on equal footing with papers. Our software is open source
under permissive licences, our methods come with reproducible workflows, and
we contribute to community standards (best-practices reviews, benchmarking
challenges, integration efforts) so that our work is useful well beyond
our own group.
</div>
</div>

For the full record, please see our [publications]({{ 'publications' | relative_url }}).
