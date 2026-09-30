# tharunkumark1.github.io

Professional profile site for **Tharun Kumar Ksheerasagar** — Senior Architect in
system architecture and performance evaluation.

The site is a single-page profile published from `index.md`, built with
[Jekyll](https://jekyllrb.com) using the
[Minimal Mistakes](https://mademistakes.com/work/jekyll-themes/minimal-mistakes/)
theme. A compiled PDF of the resume is served from
`assets/resume/` and linked as a download in the page header.

## Local development

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.

## Structure

| Path | Purpose |
| :--- | :--- |
| `index.md` | The profile page (all resume content) |
| `404.md` | Not-found page |
| `_config.yml` | Site metadata, author details, structured data (`profile:`) |
| `_data/navigation.yml` | Masthead navigation (in-page section anchors) |
| `_sass/custom.scss` | Accent colours and profile-specific styling |
| `assets/images/` | Portrait, social preview card, favicon, iOS touch icon |
| `assets/resume/` | Compiled resume PDF |
| `tools/prepare_profile_image.py` | Derives the portrait assets from `../tex` |
| `tools/generate_og_image.py` | Regenerates `og-profile.png` |
| `.github/workflows/deploy.yml` | GitHub Pages deployment from `master` |

The `tools/` directory is listed in `exclude:` in `_config.yml` so these scripts
are never published to the live site.

## Name

`site.title` in `_config.yml` is the single source of truth for the name. There
is deliberately no `masthead_title` override: the masthead falls back to
`site.title` so the two cannot drift apart. Keep the full name —
Tharun (first), Kumar (middle), Ksheerasagar (last) — rather than an
abbreviation. The favicon monogram is the one intentional short form: `TK` for
Tharun Ksheerasagar.

## Regenerating images

The portrait lives outside this repository at `../tex/Tharun_image.jpeg` and is
never committed here. Both image scripts need Pillow:

```bash
pip install pillow

# 1. portrait -> assets/images/profile.jpg (600x600) + apple-touch-icon.png (180x180)
python3 tools/prepare_profile_image.py

# 2. social card -> assets/images/og-profile.png (1200x630)
python3 tools/generate_og_image.py
```

The source is 4:5, so `prepare_profile_image.py` takes a full-width square crop
and only the vertical anchor moves. Three anchors were previewed and the default
`--offset 100` frames the head best. To try another:

```bash
python3 tools/prepare_profile_image.py --offset 200   # more headroom
```

`apple-touch-icon.png` must stay full-bleed square with no alpha and no
pre-rounded corners, because iOS applies its own squircle mask on top.

The social card composites `profile.jpg` as a circle on the right, mirroring the
hero. It falls back to text-only if the portrait is missing. Edit the `NAME_LINES`
/ `ROLE` / `LOCATION` constants at the top of the script if your title changes.

## Local overrides of theme files

The Minimal Mistakes theme is vendored, and three of its files are customised.
Upstream updates will conflict in these, so re-apply the changes when upgrading:

- `_includes/schema.html` — replaced with a richer `ProfilePage` / `Person`
  structured-data block driven by the `profile:` key in `_config.yml`
- `_includes/head/custom.html` — favicon, iOS touch icon, `theme-color`,
  `preconnect`, and a Twitter card without a handle
- `_includes/page__hero.html` — the overlay hero content is wrapped in
  `.page__hero-body`, with an optional portrait when the page sets `avatar` in
  its `header:` block. Pages without one render exactly as before
- `_layouts/single.html` — `itemtype` changed from `CreativeWork` to `ProfilePage`

The phone number is deliberately excluded from the page and the structured data;
it appears only in the linked PDF.


## Deployment

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds the site
with Jekyll and publishes it to GitHub Pages.

## License

Site content © Tharun Kumar Ksheerasagar. The Minimal Mistakes theme is
[MIT licensed](LICENSE).
