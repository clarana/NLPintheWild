---
name: GitHub Pages Setup for 11811 Course Website
description: Design for deploying the 11811 course website using Jekyll + Minima on GitHub Pages
type: project
---

# GitHub Pages Setup — 11811 Course Website

## Summary

Set up the `clarana/11811` repo for deployment via GitHub Pages using Jekyll with the Minima theme. The site will be accessible at `https://clarana.github.io/11811`. No GitHub Actions workflow is needed — GitHub Pages natively detects and builds Jekyll.

## Approach

**Option A: Native Jekyll on GitHub Pages** (chosen)

Push a valid `_config.yml` + `Gemfile` to `main`. GitHub Pages auto-detects Jekyll and builds/deploys on every push. No CI config required. Minima is on GitHub's allowed gem list.

## Repository Structure

```
11811/
├── _config.yml          ← Jekyll config (title, baseurl, theme)
├── Gemfile              ← pins github-pages gem for local/prod parity
├── index.md             ← homepage (course overview placeholder)
├── assets/
│   └── css/
│       └── custom.scss  ← Minima style overrides (initially empty)
└── .gitignore           ← excludes _site/, .bundle/, vendor/
```

## Key Configuration

- `baseurl: /11811`
- `url: https://clarana.github.io`
- `theme: minima`
- `Gemfile` pins `github-pages` gem so local preview matches deployed output

## GitHub Setup

- Enable GitHub Pages in repo settings: deploy from `main` branch, root directory
- Update local remote URL: `git remote set-url origin https://github.com/clarana/11811.git`
  (repo was renamed from `11811-site` to `11811` on GitHub)

## Local Development

```bash
bundle install
bundle exec jekyll serve
# preview at http://localhost:4000/11811
```

## Out of Scope

- Course content (schedule, readings, assignments)
- Custom domain
- GitHub Actions build pipeline (can add later if custom plugins needed)
