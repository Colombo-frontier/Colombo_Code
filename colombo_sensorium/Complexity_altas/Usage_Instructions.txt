# Complexity Atlas

This directory contains the scientific data and offline webpages for 425 optimization settings.

## Viewing the data

- Open `index.html` to browse the library.
- Current native records are in `data/settings/<setting_id>/`: `profile.json`, `identity.json`, `classification.json`, `human_tags.json`, and `machine_tags.json`.
- Current catalog and integrity bindings are in `data/derived/catalog.json` and `data/derived/catalog_sources.json`.
- PDF, TeX, and Markdown downloads are in `visualization/dist/downloads/<setting_id>/profile.*`.

Partial conclusions do not establish global optimality or exhaustive literature coverage. Scientific evidence and applicability conditions are recorded for each claim. Mathematical-font mappings in existing PDFs may limit searching or copying formulas; consult the native JSON, TeX, or Markdown for comparison.

## Rebuilding and checking

Run these commands from this directory with Python 3.11 or later. PDF checks require `pypdf` and `pdftotext`; browsing checks require Node.js.

```sh
python visualization/src/build_site_public.py --root .
node visualization/src/test-browse-engine-public.cjs
python data/tools/build_public_indexes.py --root .
python data/tools/validate_data.py
python data/tools/verify_release_public.py
```

These commands build display projections or check the current data. They do not conduct literature research, invoke models, or independently reprove cited theorems. Source dates and scholarly reference dates describe scientific provenance. Workstation backups, task receipts, and saved local test results are excluded.
