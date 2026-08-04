# Bond Biography Book

A Jupyter Book assembling the 24 enhanced bond-biography chapters from
[`../enhanced_chapters/`](../enhanced_chapters/) into a single narrative volume:
**Bond Biographies: Lives of U.S. Federal Securities, 1790–1935**.

## Layout

- `intro.md` — the book's landing page (the story of the seven parts)
- `_toc.yml` — table of contents: 7 chronological parts, 24 chapters
- `_config.yml` — book configuration (`execute_notebooks: "off"` — the notebooks are
  pre-executed and verified; their stored chart outputs are used as-is)
- `chapters/` — copies of the enhanced notebooks (the canonical versions remain in
  `../enhanced_chapters/`)
- `_build/html/` — the built book (open `_build/html/index.html` in a browser)

## Building

From this directory, with the Anaconda Python (the system Python 3.9 on this machine
has a broken PyTables/HDF5 install — not needed for the build itself, but the Anaconda
environment is the one with Jupyter Book installed):

```bash
/Users/thomassargent/anaconda3/bin/jupyter-book build .
```

Then open `_build/html/index.html`.

## Publishing to GitHub Pages

The built book is published to the repository's `gh-pages` branch and served at:

**https://maxmaxmaxmaxmaxmax373.github.io/Bond-Biographies-Generator/**

To republish after a rebuild (from this directory):

```bash
/Users/thomassargent/anaconda3/bin/ghp-import -n -p -f -m "Update book" _build/html
```

(`-n` adds `.nojekyll`, `-p` pushes, `-f` force-updates the branch. If the push fails
with an HTTP 400 "unexpected disconnect", raise the buffer once:
`git config http.postBuffer 524288000`.)

## Design notes

- Notebooks are included as `.ipynb` rather than converted to MyST markdown. MyST text
  files do not store cell outputs, so conversion would discard all rendered charts and
  force re-execution at build time (fragile, since the notebooks resolve `../data/`
  relative to their own location). Including pre-executed notebooks directly with
  execution off is the Jupyter Book–documented approach for this situation.
- To update a chapter: edit and re-execute it in `../enhanced_chapters/`, copy it into
  `chapters/`, and rebuild.
- To add a chapter: generate + enrich per `../BIOGRAPHY_AGENT_PROMPT.md`, copy the
  enhanced notebook into `chapters/`, add a line to `_toc.yml` under the right part,
  and rebuild.
- Build warnings about "non-consecutive header level" are cosmetic (some chapters use
  an H3 directly under the H1 title) and can be ignored.
