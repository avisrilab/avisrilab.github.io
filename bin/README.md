# `bin/` — site helpers

Drop-in scripts for keeping the lab website in sync with reality without
hand-editing markdown.

## `add_member.py` — add or update a lab member

Drop a photo, give a name and a role, and the People page updates itself.

```bash
# A new graduate student
bin/add_member.py ~/Downloads/jane.jpg "Jane Doe" \
    --role "Graduate Students" \
    --tagline "PhD student · single-cell modelling"

# A postdoc, with full social handles and a longer bio
bin/add_member.py ~/Downloads/sam.jpg "Sam Lee" \
    --role "Postdoctoral Researchers" \
    --tagline "Postdoc · Bayesian methods" \
    --github samlee --twitter samlee --scholar XXXXXX \
    --bio "Sam joined the lab in 2026 from ..."

# Move a former member to alumni
bin/add_member.py assets/img/people/jane-doe.jpg "Jane Doe" --role Alumni
```

What it does:

1. Copies the photo to `assets/img/people/<slug>.<ext>` (auto-cropped to a
   600×600 square if you have Pillow installed; plain copy otherwise).
2. Writes / refreshes `_people/<slug>.md` with the front-matter the People
   page renders (`role`, `tagline`, `importance`, etc.).
3. Re-running with the same name updates the front matter and photo without
   touching the bio body, so it's safe to call repeatedly.

The People page (`_pages/people.md`) groups everyone by `role` using the
order in its `role_order` front-matter list, so the new card appears in the
right section automatically the next time Jekyll rebuilds.

## `add_paper.py` — add a publication

Give it a DOI; it queries Crossref and writes a properly formatted BibTeX
entry into `_bibliography/papers.bib`. The Publications page (and the home
page strip) re-renders automatically.

```bash
# Just a DOI
bin/add_paper.py 10.1038/s41587-022-01250-0

# DOI plus a thumbnail to show in the bibliography
bin/add_paper.py 10.1038/s41592-022-01408-3 --preview ~/Downloads/fry.jpg

# If you already have a hand-built .bib entry, splice it in instead
bin/add_paper.py --bibtex ~/Downloads/manual.bib --preview ~/Downloads/fig.png
```

Behaviour:

- DOIs already in `papers.bib` are skipped (idempotent).
- Authors / journal / volume / issue / pages / year / month are pulled from
  Crossref.
- `--preview <image>` copies the image into
  `assets/img/publication_preview/` under the BibTeX key, so the al-folio
  bibliography template renders it as the entry thumbnail.

Both scripts depend only on the Python 3 standard library. Pillow is an
optional extra used by `add_member.py` for nicer photo cropping.
