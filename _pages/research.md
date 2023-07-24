---
layout: page
title: Research
permalink: /research/
nav: true
nav_order: 1
published: true
---

Welcome to Srivastava Lab, where our unwavering <u>passion</u> drives us to tackle classical biological problems in modern ways. With a particular focus on employing novel biotechnologies and customized algorithmic solutions, our team of interdisciplinary scientists is committed to delving deep into complex challenges, breaking them down into manageable subproblems, and fostering a collaborative research environment.

Our <u>profession</u> revolves around identifying key biological problems with the potential to make a significant impact. At the forefront of our research lies a comprehensive exploration of how the epigenome regulates transcription, ultimately determining cell fate. Leveraging the power of single-cell biology, we propose computational and technological solutions that pave the way for a deeper understanding of this intricate process.

Yet, our purpose goes beyond theoretical discoveries. Our <u>vocation</u> lies in the application of these proposed solutions to real-world biological problems, especially those pertaining to the chromatin dynamics of blood cell development and its aberration in malignant conditions.

At the core of our endeavors is a steadfast <u>mission</u> to foster a healthier world. With the knowledge of disease mechanisms, we are driven to unlock the secrets behind aberrant conditions. By challenging conventional approaches, we pioneer novel targets and algorithms aimed at correcting and transforming the landscape of disease.

We firmly believe that the convergence of passion, profession, vocation, and mission is the catalyst for meaningful change and we continue to push the boundaries of science under the following broad but unifying themes of research:

<font size="+2"> 1. Fast and efficient methods for bulk RNA-seq quantification</font>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/salmon_logo.png" -%}
    {% include figure.html path=profile_image_path
    class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix"> The accuracy of transcript quantification using RNA-seq data depends on many factors, such as the choice of alignment or mapping method and the quantification model. The alignment of sequencing reads to a transcriptome is a common and important step in many RNA-seq analysis tasks. While the choice of quantification model is important, considerably less attention has been given to the effect of various read alignment approaches on quantification accuracy. Thus, we investigated the influence of mapping and alignment of RNA-seq reads on the accuracy of transcript quantification and designed multiple novel alignment methodologies to overcome the shortcomings of lightweight approaches without incurring the computational cost of traditional end-to-end alignment.</div></article>
<font size="-1"> <p>* <a href="https://www.nature.com/articles/s41592-022-01408-3">He, Dongze, et al. "Alevin-fry unlocks rapid, accurate and memory-frugal quantification of single-cell RNA-seq data." Nature Methods 19.3 (2022): 316-322.</a><br>
* <a href="https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02151-8">Srivastava A., Malik L., Sarkar H., Zakeri M., Almodaresi F., Soneson C., Love MI., Kingsford C., & Patro R. (2020) "Alignment and mapping methodology influence transcript abundance estimation." Genome Biology. 2020 Dec;21(1):1-29.</a><br>
* <a href="https://arxiv.org/abs/1604.03250">Srivastava A., Sarkar H., Malik L. & Patro R. (2016) "Accurate, fast and lightweight clustering of de novo transcriptomes using fragment equivalence classes." RECOMB-seq Conference. 2016 Apr 12.</a><br>
* <a href="https://academic.oup.com/bioinformatics/article/32/12/i192/2288985">Srivastava A., Sarkar H., Gupta N. & Patro R. (2016) "RapMap: a rapid, sensitive, and accurate tool for mapping RNA-seq reads to transcriptomes." Bioinformatics. 2016 Jun 15;32(12):i192-200.</a></p></font>

<font size="+2"> 2.	Uncertainty aware Bayesian methods improves scRNA-seq quantification</font>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/alevin.jpeg" -%}
    {% include figure.html path=profile_image_path
    class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix"> There has been a steady increase in the throughput of single-cell (sc)RNA-seq experiments, facilitating experimental assay of millions of cells. Droplet based scRNA-seq experiments have a large set of gene-ambiguous reads and can commonly account for a quarter of the sequenced data, which stays largely unused by quantification methods. We designed alevin, a fast end-to-end pipeline to process scRNA-seq data, performing cell barcode detection, read mapping, UMI deduplication, gene count estimation, and cell barcode whitelisting. Alevin’s approach to UMI deduplication provides an uncertainty-aware Bayesian model to account for reads that multimap between genes. This addresses the inherent bias in existing tools which discard gene-ambiguous reads and improves the accuracy of gene abundance estimates.</div></article>
<font size="-1"> <p>* <a href="https://academic.oup.com/bioinformatics/article/38/10/2773/6564225">Mu, Wancen, et al. "Airpart: interpretable statistical models for analyzing allelic imbalance in single-cell datasets." Bioinformatics 38.10 (2022): 2773-2780.</a><br>
* <a href="https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008585">Soneson C., Srivastava A., Patro R. & Stadler MB. (2021) "Preprocessing choices affect RNA velocity results for droplet scRNA-seq data." PLOS Computational Biology. 2021 Jan 11;17(1):e1008585.</a><br>
* <a href="https://link.springer.com/article/10.1186/s13059-019-1670-y">Srivastava A., Malik L., Smith T., Sudbery I. & Patro R. (2019) "Alevin efficiently estimates accurate gene abundances from dscRNA-seq data." Genome biology. 2019 Dec;20(1):1-6.</a><br>
* <a href="https://academic.oup.com/nar/article/47/18/e105/5542870">Zhu A., Srivastava A., Ibrahim JG., Patro R. & Love MI. (2019) "Nonparametric expression analysis using inferential replicate counts." Nucleic Acids Research. 2019 Oct 10;47(18):e105.</a></p></font>

<font size="+2"> 3.	Computational Methods for single-cell analyses</font>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/scnt.png" -%}
    {% include figure.html path=profile_image_path
    class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix"> scRNA-seq data is being generated at an unprecedented pace, and the accurate estimation of gene-level abundances for each cell is a crucial first step in most scRNA-seq analyses. When pre-processing the raw scRNA-seq data to generate a count matrix, care must be taken to account for the potentially large number of multi-mapping locations per read. The sparsity of scRNA-seq data, and the strong 3’ sampling bias, make it even more challenging to disambiguate cases where there is no uniquely mapped read to any of the candidate target genes. We introduced a Bayesian framework for information sharing across cells within a sample or across multiple modalities of data to improve gene quantification estimates for scRNA-seq data.</div></article>
<font size="-1"> <p>* <a href="https://www.nature.com/articles/s41587-023-01767-y">Hao, Yuhan, et al. "Dictionary learning for integrative, multimodal and scalable single-cell analysis." Nature Biotechnology (2023): 1-12.</a><br>
* <a href="https://www.nature.com/articles/s41587-022-01250-0">Zhang, B.*, Srivastava A.*, Mimitou E., Stuart T., Raimondi I., Hao Y., Smibert P. & Satija R. (2021) "Characterizing cellular heterogeneity in chromatin state with scCUT\&Tag-pro." Nature Biotechnology 40.8 (2022): 1220-1230. </a><br>
* <a href="https://www.nature.com/articles/s41592-021-01282-5">Stuart T., Srivastava A., Lareau C. & Satija R. (2021) "Single-cell chromatin state analysis with Signac." Nature Methods (2021): 1-9.</a><br>
* <a href="https://academic.oup.com/bioinformatics/article/36/Supplement_1/i292/5870502">Srivastava A., Malik L., Sarkar H. & Patro R. (2020) "A Bayesian framework for inter-cellular information sharing improves dscRNA-seq quantification." Bioinformatics. 2020 Jul 1;36(Supplement\_1):i292-9.</a></p></font>

<font size="+2"> 4. Integrated analyses of the epigenome to understand the molecular basis of hematopoietic malignancies</font>
<article>
<div class="profile float-right">
    {%- assign profile_image_class = "img-fluid z-depth-0 rounded" -%}
    {%- assign profile_image_path = "/assets/img/publication_preview/k99.jpeg" -%}
    {% include figure.html path=profile_image_path
    class=profile_image_class alt=profile_image_path -%}
</div>
<div class="clearfix"> An impaired hematopoietic differentiation process underlies bone marrow malignancies like leukemia, but we still lack the mechanistic understanding of the sequence of regulatory events that misleads the differentiation process. Since epigenomic regulatory patterns are major features of leukemic development, understanding the chromatin dynamics of a failed (malignant) hematopoietic differentiation process can help define the molecular basis of leukemia. A prerequisite to such an understanding is a framework that allows investigation of the progressive changes in the activity of the regulatory elements (RE) during hematopoietic differentiation. Single-cell CUT&Tag (scCUT&Tag) technology is well-suited for such studies as RE activity through histone modification profiles can be investigated in a lineage-specific manner. Using scCUT&Tag we will investigate the RE and progressive changes in their activity during hematopoiesis. First, we will define a multimodal reference mapping framework for mouse hematopoiesis. This framework will allow us to integrate multiple histone modification profiles onto one reference and compare the chromatin states of the RE between a wild type (WT) and mouse model with loss of function in histone methyl transferase (HMT). Second, since HMTs regulate transcription through the interaction network of RE. We will define a chromatin state aware map that dynamically links REs across developmental trajectories. We will use this framework to investigate the changes in the interaction of REs due to HMT loss. Third, since the transcriptional state of a cell emerges from the underlying gene regulatory network (GRN), We will integrate single-cell gene expression data with histone modification profiles and extend it to define a chromatin state aware model of GRN. We will compare the WT and HMT loss experiments and define the differential GRN.</div></article>
<font size="-1"> <p>* <a href="https://reporter.nih.gov/project-details/10538621">Srivastava A. (2020) "Integrated analyses of the epigenome to understand the molecular basis of hematopoietic malignancies.", Project Number: K99CA267677.</a></p></font>


          