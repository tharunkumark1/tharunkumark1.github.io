# tharunkumark1.github.io

Professional profile site for **Tharun Kumar Ksheerasagar** — Senior Architect in
system architecture and hardware simulation.

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
| `_data/navigation.yml` | Masthead navigation |
| `_sass/custom.scss` | Accent colours and profile-specific styling |
| `assets/images/` | Social preview card and favicon |
| `assets/resume/` | Compiled resume PDF |
| `tools/generate_og_image.py` | Regenerates `og-profile.png` |
| `.github/workflows/deploy.yml` | GitHub Pages deployment from `master` |

## Regenerating the social preview card

```bash
pip install pillow
python3 tools/generate_og_image.py
```

Edit the `NAME` / `ROLE` / `LOCATION` constants at the top of the script if your
title changes.

## Local overrides of theme files

The Minimal Mistakes theme is vendored, and three of its files are customised.
Upstream updates will conflict in these, so re-apply the changes when upgrading:

- `_includes/schema.html` — replaced with a richer `ProfilePage` / `Person`
  structured-data block driven by the `profile:` key in `_config.yml`
- `_includes/head/custom.html` — favicon, `theme-color`, `preconnect`, and a
  Twitter card without a handle
- `_layouts/single.html` — `itemtype` changed from `CreativeWork` to `ProfilePage`

The phone number is deliberately excluded from the page and the structured data;
it appears only in the linked PDF.


## Deployment

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds the site
with Jekyll and publishes it to GitHub Pages.

## License

Site content © Tharun Kumar Ksheerasagar. The Minimal Mistakes theme is
[MIT licensed](LICENSE).
