Generators for the site's images. .github/ is not published, so nothing here goes live.

art.py        header-dots.svg, benchdrop.svg, bagpiper.svg (the dot-art icons)
              python3 .github/tools/art.py assets/img/art
              matisse.svg was drawn separately with a seeded script, not by art.py.
og.html       the 1200x630 link-preview card (assets/img/og-card.jpg), drawn on a canvas
icon.html     the 180x180 apple-touch-icon (assets/img/apple-touch-icon.png)
save_server.py  lets og.html / icon.html save their PNG: run it, then open the page in a browser
              python3 .github/tools/save_server.py /absolute/path/out.png   (serves http://127.0.0.1:8766)
              then shrink to JPEG where needed, e.g. sips -s format jpeg -s formatOptions 82 in.png --out out.jpg
