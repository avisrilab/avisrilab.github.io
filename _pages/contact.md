---
layout: page
permalink: /contact/
title: Join/Contact
published: true
# description: Materials for courses you taught. Replace this text with your description.
nav: true
nav_order: 4
funders: true
---

We constantly seek out exceptional individuals with diverse backgrounds and expertise in various fields, such as mathematics, biology, computer science, and related disciplines. Learn more about our lab's <a href="{{ 'research' | relative_url }}">research</a> and explore our extensive list of <a href="{{ 'publications' | relative_url }}">publications</a>. If our work captivates your interest, don't hesitate to get in touch with Avi via <a href="mailto:asrivastava@wistar.org">email</a> or Twitter (<a href="https://twitter.com/k3yavi">@k3yavi</a>).

<div class="row justify-content-sm-center">
  <div class="col-sm-10 mt-3 mt-md-0">
      {% include figure.html path="/assets/img/publication_preview/phily.jpeg" title="phily" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-4 mt-3 mt-md-0">
      {% include figure.html path="/assets/img/publication_preview/wistar.jpg" title="wistar" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-6 mt-3 mt-md-0">
      <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3058.5712824403263!2d-75.19819272374848!3d39.95097837151828!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c6c6598069e279%3A0x184000160e8fb50e!2sThe%20Wistar%20Institute!5e0!3m2!1sen!2sus!4v1685149671130!5m2!1sen!2sus" width="300" height="225" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</div>


<font size="+2">Contact</font>
<p>Dr. Avi Srivastava <br>
  <a href="mailto:asrivastava@wistar.org">asrivastava@wistar.org</a> <br>
  (<a href="{{ 'people/avi' | relative_url }}">Alternate ways to connect</a>)
</p>

<p> Srivastava lab<br>
The Wistar Institute<br>
3601 Spruce Street<br>
Philadelphia, Pennsylvania 19104</p>

<div class="social">
  <div class="contact-icons">
    {% include social.html %}
  </div>

  <div class="contact-note">
    {{ site.contact_note }}
  </div>
</div>

<!-- Funders -->
{%- if page.funders %}
<center><font size="+1">The Srivastava Lab is funded by the generous support of</font></center><br>
<div class="row justify-content-sm-center">
  <div class="col-sm-4 mt-3 mt-md-0">
    {% include figure.html path="/assets/img/nci.svg" class="img-fluid rounded z-depth-0" %}
  </div>
</div>
{%- endif %}
