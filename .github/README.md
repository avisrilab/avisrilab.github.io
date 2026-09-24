# Srivastava Lab website

Source for [avisrilab.org](https://avisrilab.org). Plain HTML, CSS and JavaScript with no build
step. Lists (news, people, papers, tools) live in `data/*.json`, and `js/lab.js` turns them into
the pages. This file sits in `.github/`, which is never published; everything in the repo root is.

## Publish

1. Run `python3 .github/scripts/check_site.py`. It names the file and the problem if an edit is
   broken.
2. Push `master`. The deploy workflow runs the same check, then copies the repo to `gh-pages`. If
   the check fails, nothing is deployed and the live site keeps its last good version; the error is
   in the Actions tab.
3. Browsers cache pages for 10 minutes (`cache-control: max-age=600`). Hard-reload to see a change.

## Preview locally

```sh
python3 -m http.server 8765
```

Then open <http://localhost:8765>. Opening an HTML file directly shows no lists: the pages fetch
`data/*.json`, which needs a server.

## Add content

- **News item.** Add `{"date": "YYYY-MM", "text": "..."}` anywhere in `data/news.json`; the page
  sorts by date. `text` is HTML, so links are `<a href="...">`.
- **Person.** Add `{"id", "name", "role", "status", "tagline", "photo"}` to `data/people.json`.
  `role` is one of `Postdoctoral Researchers`, `Graduate Students`, `Research Assistants`,
  `Rotation Students`, `Undergraduate Researchers`, `Visiting Scientists`, in that page order
  (`roleOrder` in lab.js; a new role goes there and in `ROLES` in the check). `status` is
  `current` or `alumni`. `photo` is optional (`assets/img/people/<id>.jpg`, square); without it
  the card shows initials. `tagline` replaces the role under the name.
- **Paper.** Add `{"id", "title", "authors", "journal", "year", "doi", "preview"}` to
  `data/papers.json`. `year` is a number, `doi` has no `https://doi.org/`, `authors` is a list.
  Papers group by year, in file order within a year. `preview` is optional
  (`assets/img/publication_preview/`).
- **Tool.** Add an object to `data/tools.json` with every field `toolCard` uses (copy an existing
  entry; use `null` or `[]` for none). File order is page order. The icon is a 120x120 SVG in
  `assets/img/art/` with literal hex colours, because an `<img>` cannot use the site's CSS
  variables. Then `grep -n -i '<Name>' *.html` for the places that name every tool (the home
  stepper, the Research block, meta descriptions).
- **Matisse vignette.** In the Matisse repo, add `vignettes/<slug>.Rmd` and one line in the
  `_pkgdown.yml` articles menu, then push. Add `{title, path, blurb}` to the Matisse `vignettes`
  in `data/tools.json` only after `avisrilab.org/Matisse/articles/<slug>.html` loads.
- **Page text.** Edit the HTML. The nav and footer must stay identical on all six pages. A new
  page also needs its canonical and `og:url` tags, a `sitemap.xml` entry, and a line in `PAGES`
  in the check script.

## Content rules

- Published or public work only: no unpublished results, no grant numbers, no job ads.
- No long dashes anywhere (the check fails on them). Use a comma, colon or period.
- In prose, prefer "process", "detect" or "map" over the verb "read".

## Mistakes the check does not catch

| Mistake | What you see |
|---|---|
| Vignette or `/Matisse/` link added before the docs page is live | A dead link |
| PI entry missing `title`, `institution` or `bio` | "undefined" on the People page |
| Your name spelled other than "Avi Srivastava" in an author list | The name is not bold |
| A bare `<` in any text field | Broken layout |
| An icon SVG that uses `var(...)` colours | A black or blank icon |
| Checking right after a push | The old page, for up to 10 minutes |

Image generators (dot-art icons, the link-preview card) are described in `.github/tools/README.txt`.
