# Webpage for #SrivastavaLab at the Wistar Institute

Drop-in tooling (bin/) — both standard-library Python 3, executable, smoke-tested.

bin/add_member.py — drop a photo, get a card:

bin/add_member.py ~/Downloads/jane.jpg "Jane Doe" \
    --role "Graduate Students" \
    --tagline "PhD student · single-cell modelling"

Copies the photo into assets/img/people/<slug>.<ext> (auto-cropped to a 600×600 square if Pillow is installed; plain copy otherwise).
Generates / refreshes _people/<slug>.md with the front-matter the People page uses.
Idempotent: re-running with the same name updates the card without clobbering an existing bio body.
Move someone to alumni later by re-running with --role Alumni.
bin/add_paper.py — drop a DOI, get a publication:

bin/add_paper.py 10.1038/s41587-022-01250-0
bin/add_paper.py 10.1038/s41592-022-01408-3 --preview ~/Downloads/fry.jpg
bin/add_paper.py --bibtex ~/Downloads/manual.bib

Queries Crossref for full metadata and writes a jekyll-scholar BibTeX entry to _bibliography/papers.bib.
DOIs already in the file are skipped (idempotent; the duplicate check runs before the network call).
--preview copies a thumbnail into assets/img/publication_preview/ so it shows up next to the entry.
--bibtex lets you splice in a hand-built entry instead of fetching.
bin/README.md documents both flows.

Local preview
The repo's GitHub Pages workflow uses Ruby 3.2.1; your system Ruby is 2.6 and bundler isn't installed under it, so I didn't run the build here. To preview locally, the standard al-folio flow works (the project also ships a docker-compose option):

# In the repo root: /Users/avisrivastava/Code/avisrilab.github.io
bundle install                          # one-time, installs the gems in Gemfile
bundle exec jekyll serve --livereload   # then open http://127.0.0.1:4000

If you don't want to manage Ruby locally, the project's docker setup does the same thing without touching system Ruby:

docker compose -f docker-local.yml up   # serves on http://localhost:8080

(That's the same image al-folio's upstream uses for its own preview.)
