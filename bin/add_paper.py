#!/usr/bin/env python3
"""Drop-in helper to add a new publication.

Given a DOI (or a raw BibTeX file), this script:
  1. Queries the public Crossref REST API to pull rich metadata (title,
     authors, journal, year, month, volume, issue, pages, publisher).
  2. Renders that into a jekyll-scholar-friendly BibTeX entry.
  3. Appends the entry to ``_bibliography/papers.bib`` if a matching DOI
     isn't already there. The Publications page rebuilds automatically.
  4. Optionally copies a preview image into ``assets/img/publication_preview/``
     and references it via the ``preview = {...}`` field that the al-folio
     bibliography template renders next to each entry.

Typical usage::

    bin/add_paper.py 10.1038/s41587-022-01250-0
    bin/add_paper.py 10.1038/s41592-022-01408-3 --preview ~/Downloads/fry.jpg
    bin/add_paper.py --bibtex ~/Downloads/manual.bib

This uses only the standard library so it works on any reasonably recent
Python 3 install.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_PATH = REPO_ROOT / "_bibliography" / "papers.bib"
PREVIEW_DIR = REPO_ROOT / "assets" / "img" / "publication_preview"

CROSSREF_URL = "https://api.crossref.org/works/{doi}"
USER_AGENT = "SrivastavaLabSite/1.0 (mailto:asrivastava@wistar.org)"

MONTHS = {
    1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
    7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec",
}


def slugify(text: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "", text or "")
    return s or "paper"


def fetch_crossref(doi: str) -> dict:
    url = CROSSREF_URL.format(doi=urllib.parse.quote(doi, safe="/"))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"crossref lookup failed for {doi}: HTTP {e.code}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"crossref lookup failed for {doi}: {e.reason}") from e
    if data.get("status") != "ok":
        raise SystemExit(f"crossref returned non-ok status for {doi}: {data}")
    return data["message"]


def _format_authors(authors: list[dict]) -> str:
    parts = []
    for a in authors or []:
        given = (a.get("given") or "").strip()
        family = (a.get("family") or "").strip()
        if family and given:
            parts.append(f"{given} {family}")
        elif family:
            parts.append(family)
    return " and ".join(parts)


def _first_year_month(work: dict) -> tuple[int | None, int | None]:
    for key in ("published-print", "published-online", "issued", "created"):
        date_parts = (work.get(key) or {}).get("date-parts") or []
        if date_parts and date_parts[0]:
            year = date_parts[0][0] if len(date_parts[0]) >= 1 else None
            month = date_parts[0][1] if len(date_parts[0]) >= 2 else None
            return year, month
    return None, None


def crossref_to_bibtex(work: dict, preview: str | None = None) -> tuple[str, str]:
    """Return (bibtex_key, bibtex_entry) for a Crossref work record."""
    authors = work.get("author") or []
    first_family = ""
    for a in authors:
        if a.get("family"):
            first_family = a["family"]
            break
    year, month = _first_year_month(work)

    key = f"{slugify(first_family)}{year or ''}".strip() or "paper"

    title = " ".join((work.get("title") or [""])[0].split()) or "Untitled"
    journal = " ".join((work.get("container-title") or [""])[0].split())
    publisher = work.get("publisher", "")
    volume = work.get("volume", "")
    issue = work.get("issue", "")
    pages = work.get("page", "")
    doi = work.get("DOI", "")
    url = work.get("URL") or (f"https://doi.org/{doi}" if doi else "")

    fields: list[tuple[str, str]] = [
        ("doi", doi),
        ("url", url),
        ("year", str(year) if year else ""),
    ]
    if month and 1 <= month <= 12:
        fields.append(("month", MONTHS[month]))
    fields.extend([
        ("publisher", publisher),
        ("volume", volume),
        ("number", issue),
        ("pages", pages),
        ("author", _format_authors(authors)),
        ("title", title),
        ("journal", journal),
    ])
    if preview:
        fields.append(("preview", preview))

    lines = [f"@article{{{key},"]
    for field, value in fields:
        if value is None or value == "":
            continue
        # Wrap braces around values that contain BibTeX-significant chars.
        lines.append(f"  {field} = {{{value}}},")
    # Drop trailing comma on the last field.
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return key, "\n".join(lines) + "\n"


def parse_bibtex_first_entry(text: str) -> tuple[str, str, str | None]:
    """Return (key, full_entry, doi_if_present) for the first @entry in `text`."""
    match = re.search(r"@\w+\s*\{\s*([^,\s]+)\s*,", text)
    if not match:
        raise SystemExit("could not find a BibTeX @entry in the file.")
    key = match.group(1)
    # Extract the balanced { ... } body of the entry.
    start = text.find("{", match.start())
    depth = 0
    end = -1
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end == -1:
        raise SystemExit("malformed BibTeX entry (unbalanced braces).")
    entry = text[match.start():end] + "\n"
    doi_match = re.search(r"doi\s*=\s*\{([^}]+)\}", entry, re.IGNORECASE)
    doi = doi_match.group(1).strip() if doi_match else None
    return key, entry, doi


def already_present(doi: str | None) -> bool:
    if not doi:
        return False
    if not BIB_PATH.exists():
        return False
    contents = BIB_PATH.read_text(encoding="utf-8")
    return doi.lower() in contents.lower()


def append_entry(entry: str) -> None:
    BIB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if BIB_PATH.exists():
        existing = BIB_PATH.read_text(encoding="utf-8")
        if not existing.endswith("\n"):
            existing += "\n"
        new_contents = existing + "\n" + entry
    else:
        new_contents = "---\n---\n\n" + entry
    BIB_PATH.write_text(new_contents, encoding="utf-8")


def copy_preview(preview_path: Path, key: str) -> str:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    ext = preview_path.suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        ext = ".jpg"
    dest = PREVIEW_DIR / f"{key}{ext}"
    shutil.copyfile(preview_path, dest)
    return dest.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a publication to the bibliography.")
    parser.add_argument("doi", nargs="?", help="DOI of the paper to add.")
    parser.add_argument(
        "--bibtex",
        type=Path,
        default=None,
        help="Path to an existing .bib file to splice in instead of fetching from Crossref.",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=None,
        help="Optional preview image (JPG/PNG/WebP) to copy into assets/img/publication_preview/.",
    )
    args = parser.parse_args()

    if not args.doi and not args.bibtex:
        parser.error("either a DOI or --bibtex <file> is required.")

    if args.bibtex:
        text = args.bibtex.read_text(encoding="utf-8")
        key, entry, doi = parse_bibtex_first_entry(text)
        if args.preview:
            preview_name = copy_preview(args.preview, key)
            if "preview" not in entry.lower():
                entry = entry.rstrip("}\n") + f",\n  preview = {{{preview_name}}}\n}}\n"
        if already_present(doi):
            print(f"[skip] DOI {doi} already in {BIB_PATH.name}")
            return 0
        append_entry(entry)
        print(f"added BibTeX entry '{key}' to {BIB_PATH.relative_to(REPO_ROOT)}")
        return 0

    if already_present(args.doi):
        print(f"[skip] DOI {args.doi} already in {BIB_PATH.name}")
        return 0
    work = fetch_crossref(args.doi)

    preview_name = None
    if args.preview and args.preview.exists():
        # Use a temporary key for the file name; we'll rename if needed below.
        first_family = ""
        for a in work.get("author") or []:
            if a.get("family"):
                first_family = a["family"]
                break
        year, _ = _first_year_month(work)
        tmp_key = f"{slugify(first_family)}{year or ''}".strip() or "paper"
        preview_name = copy_preview(args.preview, tmp_key)

    key, entry = crossref_to_bibtex(work, preview=preview_name)
    append_entry(entry)
    print(f"added BibTeX entry '{key}' (DOI {args.doi}) to {BIB_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
