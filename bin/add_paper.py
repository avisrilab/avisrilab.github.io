#!/usr/bin/env python3
"""
add_paper.py — add a paper to data/papers.json via DOI

Usage
-----
  python3 bin/add_paper.py 10.1038/s41587-022-01250-0
  python3 bin/add_paper.py 10.1038/s41592-022-01408-3 --preview ~/Downloads/fry.jpg --selected

Fetches metadata from the Crossref API, then appends a new entry to
data/papers.json.  If a paper with the same DOI already exists it is
skipped (idempotent).

After running, commit data/papers.json (and any new preview image) to publish.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
PAPERS_JSON = REPO_ROOT / "data" / "papers.json"
PREVIEW_DIR = REPO_ROOT / "assets" / "img" / "publication_preview"

CROSSREF_URL = "https://api.crossref.org/works/{doi}"
USER_AGENT   = "SrivastavaLabSite/1.0 (mailto:asrivastava@wistar.org)"


def fetch_crossref(doi: str) -> dict:
    url = CROSSREF_URL.format(doi=urllib.parse.quote(doi, safe="/"))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Crossref lookup failed for {doi}: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Crossref lookup failed for {doi}: {exc.reason}") from exc
    if data.get("status") != "ok":
        raise SystemExit(f"Crossref returned non-ok for {doi}")
    return data["message"]


def parse_authors(work: dict) -> list[str]:
    out = []
    for a in work.get("author") or []:
        given  = (a.get("given")  or "").strip()
        family = (a.get("family") or "").strip()
        if given and family:
            out.append(f"{given} {family}")
        elif family:
            out.append(family)
    return out


def first_year(work: dict) -> int | None:
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (work.get(key) or {}).get("date-parts") or []
        if parts and parts[0]:
            return parts[0][0]
    return None


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-") or "paper"


def copy_preview(src: Path, slug: str) -> str:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    dest = PREVIEW_DIR / f"{slug}.jpg"
    try:
        from PIL import Image, ImageOps  # type: ignore
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            im = im.convert("RGB")
            im.thumbnail((600, 400), Image.LANCZOS)
            im.save(dest, "JPEG", quality=88)
        print(f"  ✓ Preview saved → {dest.relative_to(REPO_ROOT)}")
    except ImportError:
        shutil.copy2(src, dest)
        print(f"  ✓ Preview copied → {dest.relative_to(REPO_ROOT)}")
    return f"assets/img/publication_preview/{slug}.jpg"


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a paper to data/papers.json via DOI.")
    parser.add_argument("doi",        help="Paper DOI, e.g. 10.1038/s41592-022-01408-3")
    parser.add_argument("--preview",  type=Path, default=None, help="Preview image file")
    parser.add_argument("--selected", action="store_true",     help="Mark as a highlighted paper")
    args = parser.parse_args()

    # Load existing
    papers = json.loads(PAPERS_JSON.read_text()) if PAPERS_JSON.exists() else []

    # Idempotency check
    doi_clean = args.doi.lstrip("https://doi.org/").strip()
    if any(p.get("doi", "").lower() == doi_clean.lower() for p in papers):
        print(f"  [skip] DOI {doi_clean} already in papers.json")
        return 0

    print(f"  Fetching metadata for {doi_clean} …")
    work    = fetch_crossref(doi_clean)
    authors = parse_authors(work)
    year    = first_year(work)
    title   = " ".join((work.get("title") or [""])[0].split())
    journal = " ".join((work.get("container-title") or [""])[0].split())

    # Build a stable slug for the id / preview filename
    first_family = ""
    for a in work.get("author") or []:
        if a.get("family"):
            first_family = a["family"]
            break
    slug = slugify(f"{first_family}{year or ''}")

    preview_path = ""
    if args.preview:
        src = args.preview.resolve()
        if not src.exists():
            print(f"  Warning: preview file not found: {src}", file=sys.stderr)
        else:
            preview_path = copy_preview(src, slug)

    entry = {
        "id":       slug,
        "title":    title,
        "authors":  authors,
        "journal":  journal,
        "year":     year,
        "doi":      doi_clean,
        "selected": args.selected,
    }
    if preview_path:
        entry["preview"] = preview_path

    papers.append(entry)

    # Sort by year descending, then title
    papers.sort(key=lambda p: (-(p.get("year") or 0), p.get("title", "")))

    PAPERS_JSON.write_text(json.dumps(papers, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✓ Added '{title}' ({year}) to data/papers.json")
    print(f"  → Commit data/papers.json" + (f" and {preview_path}" if preview_path else "") + " to publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
