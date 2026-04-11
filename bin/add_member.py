#!/usr/bin/env python3
"""Drop-in helper to add (or update) a lab member.

Given a photo and a name, this script:
  1. Copies the photo into ``assets/img/people/<slug>.<ext>`` (resizing it to
     a sensible square thumbnail if Pillow is installed).
  2. Generates ``_people/<slug>.md`` with the front-matter the People page
     expects (``role``, ``tagline``, ``importance``, etc.), so the new card
     appears automatically the next time Jekyll rebuilds.

It is *idempotent*: running it again with the same name will refresh the
photo and bump any new fields you pass on the command line, without
clobbering the body of the existing markdown file.

Typical usage::

    bin/add_member.py ~/Downloads/jane.jpg "Jane Doe" \
        --role "Graduate Students" \
        --tagline "PhD student · single-cell modelling" \
        --bio "Jane joined the lab in 2026 after ..."

When the member moves on, run::

    bin/add_member.py ~/Downloads/jane.jpg "Jane Doe" --role Alumni

and the card moves to the Alumni section. Only standard library is required.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PEOPLE_DIR = REPO_ROOT / "_people"
PHOTO_DIR = REPO_ROOT / "assets" / "img" / "people"

VALID_ROLES = [
    "Principal Investigator",
    "Postdoctoral Researchers",
    "Graduate Students",
    "Research Assistants",
    "Undergraduate Researchers",
    "Visiting Scientists",
    "Alumni",
]

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "member"


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Tiny YAML-ish parser for the simple key: value front matter we emit."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    fm: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm, text[match.end():]


def render_front_matter(fm: dict[str, str]) -> str:
    out = ["---"]
    for key, value in fm.items():
        if value is None or value == "":
            continue
        out.append(f"{key}: {value}")
    out.append("---")
    return "\n".join(out) + "\n"


def copy_photo(src: Path, slug: str) -> Path:
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".jpg"
    dest = PHOTO_DIR / f"{slug}{ext}"

    # If Pillow is available, resize to a 600x600 square crop. Otherwise,
    # just copy the file as-is.
    try:
        from PIL import Image, ImageOps  # type: ignore
    except Exception:
        shutil.copyfile(src, dest)
        return dest

    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im = ImageOps.fit(im, (600, 600), method=Image.LANCZOS)
        if ext in (".jpg", ".jpeg"):
            im = im.convert("RGB")
        im.save(dest)
    return dest


def upsert_member(
    name: str,
    photo_path: Path,
    role: str,
    tagline: str | None,
    importance: int,
    bio: str | None,
    email: str | None,
    twitter: str | None,
    github: str | None,
    scholar: str | None,
    orcid: str | None,
    linkedin: str | None,
) -> Path:
    if role not in VALID_ROLES:
        print(
            f"[warn] role '{role}' is not in the standard list; it will still "
            f"render under a 'Lab members' section.",
            file=sys.stderr,
        )

    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(name)
    md_path = PEOPLE_DIR / f"{slug}.md"

    photo = copy_photo(photo_path, slug)
    rel_photo = photo.relative_to(REPO_ROOT).as_posix()

    fm: dict[str, str] = {}
    body = ""
    if md_path.exists():
        existing = md_path.read_text(encoding="utf-8")
        fm, body = parse_front_matter(existing)

    fm["layout"] = "page"
    fm["title"] = name
    fm["description"] = fm.get("description") or f"{role} · Srivastava Lab"
    fm["img"] = rel_photo
    fm["role"] = role
    if tagline:
        fm["tagline"] = tagline
    fm["importance"] = str(importance)
    fm["category"] = fm.get("category") or "[Team]"
    if email:
        fm["email"] = email
    if twitter:
        fm["twitter_username"] = twitter
    if github:
        fm["github_username"] = github
    if scholar:
        fm["scholar_userid"] = scholar
    if orcid:
        fm["orcid_id"] = orcid
    if linkedin:
        fm["linkedin_username"] = linkedin

    if not body.strip():
        body = (
            f"\n<div class=\"row\">\n"
            f"    <div class=\"col-sm-4 mt-3 mt-md-0\">\n"
            f"        {{% include figure.html path=\"{rel_photo}\" "
            f"title=\"{name}\" class=\"img-fluid rounded z-depth-1\" %}}\n"
            f"    </div>\n"
            f"</div>\n\n"
        )
        if bio:
            body += bio.strip() + "\n"
        else:
            body += f"{name} is a {role.rstrip('s')} in the Srivastava Lab.\n"
    elif bio:
        # Append the new bio paragraph rather than overwriting an existing body.
        body = body.rstrip() + "\n\n" + bio.strip() + "\n"

    md_path.write_text(render_front_matter(fm) + body, encoding="utf-8")
    return md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Add or update a lab member.")
    parser.add_argument("photo", type=Path, help="Path to the member's photo.")
    parser.add_argument("name", help='Full name, e.g. "Jane Doe".')
    parser.add_argument(
        "--role",
        default="Graduate Students",
        help="Section to file the member under (one of the standard roles).",
    )
    parser.add_argument("--tagline", default=None, help="Short subtitle on the card.")
    parser.add_argument(
        "--importance",
        type=int,
        default=10,
        help="Sort order within a role section (lower = first).",
    )
    parser.add_argument("--bio", default=None, help="Free-form bio paragraph.")
    parser.add_argument("--email", default=None)
    parser.add_argument("--twitter", default=None)
    parser.add_argument("--github", default=None)
    parser.add_argument("--scholar", default=None, help="Google Scholar user id.")
    parser.add_argument("--orcid", default=None)
    parser.add_argument("--linkedin", default=None)

    args = parser.parse_args()

    if not args.photo.exists():
        print(f"error: photo not found: {args.photo}", file=sys.stderr)
        return 2

    md_path = upsert_member(
        name=args.name,
        photo_path=args.photo,
        role=args.role,
        tagline=args.tagline,
        importance=args.importance,
        bio=args.bio,
        email=args.email,
        twitter=args.twitter,
        github=args.github,
        scholar=args.scholar,
        orcid=args.orcid,
        linkedin=args.linkedin,
    )
    print(f"wrote {md_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
