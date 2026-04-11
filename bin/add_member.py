#!/usr/bin/env python3
"""
add_member.py — add a new lab member to data/people.json

Usage
-----
  python3 bin/add_member.py --name "Jane Doe" \\
                             --role "Graduate Students" \\
                             --tagline "RNA-seq · chromatin biology" \\
                             --photo ~/Downloads/jane.jpg

Valid roles
-----------
  Principal Investigator | Postdoctoral Researchers | Graduate Students
  Research Assistants | Undergraduate Researchers | Visiting Scientists

After running, commit the updated data/people.json and any new image.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
PEOPLE_JSON = REPO_ROOT / "data" / "people.json"
IMG_DIR     = REPO_ROOT / "assets" / "img" / "people"

ROLE_ORDER = [
    "Principal Investigator",
    "Postdoctoral Researchers",
    "Graduate Students",
    "Research Assistants",
    "Undergraduate Researchers",
    "Visiting Scientists",
    "Alumni",
]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-") or "member"


def copy_photo(src: Path, slug: str) -> str:
    """Copy (and optionally resize) photo; return repo-relative path."""
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    dest = IMG_DIR / f"{slug}.jpg"
    try:
        from PIL import Image, ImageOps  # type: ignore
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            im = ImageOps.fit(im.convert("RGB"), (400, 400), Image.LANCZOS)
            im.save(dest, "JPEG", quality=88)
        print(f"  ✓ Photo resized → {dest.relative_to(REPO_ROOT)}")
    except ImportError:
        shutil.copy2(src, dest)
        print(f"  ✓ Photo copied (install Pillow for auto-resize) → {dest.relative_to(REPO_ROOT)}")
    return f"assets/img/people/{slug}.jpg"


def main() -> int:
    parser = argparse.ArgumentParser(description="Add or update a lab member.")
    parser.add_argument("--name",    required=True, help="Full name")
    parser.add_argument("--role",    required=True, help="Role / section")
    parser.add_argument("--tagline", default="",    help="Short subtitle on the card")
    parser.add_argument("--bio",     default="",    help="Bio paragraph (optional)")
    parser.add_argument("--photo",   type=Path,     help="Path to photo file")
    parser.add_argument("--email",   default="")
    parser.add_argument("--github",  default="")
    parser.add_argument("--twitter", default="")
    parser.add_argument("--scholar", default="")
    parser.add_argument("--orcid",   default="")
    parser.add_argument("--linkedin",default="")
    parser.add_argument("--status",  default="current", choices=["current", "alumni"])
    args = parser.parse_args()

    if args.role not in ROLE_ORDER:
        print(f"Warning: role '{args.role}' is not in the standard list.")

    slug   = slugify(args.name)
    people = json.loads(PEOPLE_JSON.read_text()) if PEOPLE_JSON.exists() else []

    # Remove existing entry with same id (upsert)
    people = [p for p in people if p.get("id") != slug]

    photo_path = ""
    if args.photo:
        src = args.photo.resolve()
        if not src.exists():
            print(f"Error: photo not found: {src}", file=sys.stderr)
            return 2
        photo_path = copy_photo(src, slug)

    entry: dict = {"id": slug, "name": args.name, "role": args.role, "status": args.status}
    for field in ("photo", "tagline", "bio", "email", "github", "twitter", "scholar", "orcid", "linkedin"):
        val = photo_path if field == "photo" else getattr(args, field)
        if val:
            entry[field] = val

    people.append(entry)

    # Sort by role order, then name
    people.sort(key=lambda p: (
        ROLE_ORDER.index(p["role"]) if p.get("role") in ROLE_ORDER else len(ROLE_ORDER),
        p.get("name", "")
    ))

    PEOPLE_JSON.write_text(json.dumps(people, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✓ '{args.name}' ({args.role}) written to data/people.json")
    print(f"  → Commit data/people.json" + (f" and {photo_path}" if photo_path else "") + " to publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
