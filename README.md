# 11-811 course website

Source for **<https://nlpinthewild.clarasna.com>** — *11-811: Interdisciplinary NLP* (CMU, Fall 2026).

Built with [Jekyll](https://jekyllrb.com) and the [Just the Docs](https://just-the-docs.com) theme.
Every push to `main` is automatically built and deployed by GitHub Actions
(`.github/workflows/pages.yml`). **If a build fails, the previous site stays up** — a broken
edit can't take the site down.

The rest of this file is a practical guide to editing the site, for instructors and for
students who'd like to suggest content.

## Where things live

| To change… | Edit… |
|---|---|
| Home page (overview, logistics, schedule, assignment summaries, policies) | `index.md` |
| Readings & resources | `readings.md` |
| A lab or the project | `_labs/lab1.md` … `_labs/lab4.md`, `_labs/project.md` |
| The schedule (dates, topics, links) | `_data/schedule.yml` |
| Lecture slides / handouts | add files under `assets/slides/`, then link them from `_data/schedule.yml` |
| Navigation, theme, site-wide settings | `_config.yml` |

Everything is Markdown, so most edits are just writing text.

## Common edits

**Change a due date or points.** Edit the front matter (the `key: value` block at the top) of
the assignment's file in `_labs/`. For example, in `_labs/lab1.md`:

```yaml
---
title: "Lab 1"
due: 2026-09-10     # ← change here; updates the Lab page AND its home-page summary
points: 9
---
```

**Write or expand an assignment.** In `_labs/<name>.md`, the text **above** the `<!--more-->`
line is the short summary shown on the home page; everything **below** it shows only on the
assignment's own page:

```markdown
One or two sentences summarizing the assignment. (Shown on the home page.)
<!--more-->

## Instructions

The full write-up. (Shown only on the Lab's own page.)
```

Edit one file, and the summary and the full version stay in sync.

**Add a class session, reading, or slides.** Edit `_data/schedule.yml`. Each list item is one
class:

```yaml
- week: 3
  date: 2026-09-08
  topic: "Topic goes here"
  slides: /assets/slides/2026-09-08-topic.pdf   # optional
```

**Add a new page.** Create `mypage.md` starting with:

```yaml
---
layout: default
title: "My Page"
nav_order: 5        # position in the sidebar
---
```

**Hide a page until it's ready.** Add `nav_exclude: true` (keeps it off the sidebar) or
`published: false` (leaves it out of the build entirely).

## Suggesting a change — no setup required

You can propose an edit entirely in the browser, with nothing to install. This is the
recommended path for students, and for quick fixes:

1. On any page of the live site, click **"Edit this page on GitHub"** at the bottom — or open
   the file here in the repo and click the ✏️ pencil.
2. Make your changes in the editor.
3. Click **Commit changes / Propose changes**. GitHub will walk you through opening a **pull
   request** (creating a fork or branch for you automatically if needed).

An instructor reviews and merges it; the site updates on merge.

## Previewing locally (for bigger edits)

For substantial changes, it's worth previewing before you publish. You need **Ruby 3.x** (your
macOS system Ruby may be too old) and Bundler. If you don't have a modern Ruby, the easiest route is
[rbenv](https://github.com/rbenv/rbenv):

```bash
brew install rbenv ruby-build
rbenv install 3.3.6 && rbenv global 3.3.6
```

Then, from the repo root:

```bash
gem install bundler
bundle install
bundle exec jekyll serve --livereload
```

Open **<http://localhost:4000>**. Files rebuild as you save them, and build errors (bad
Markdown, YAML, etc.) print in that terminal with the file and line. To check that it builds
without serving: `bundle exec jekyll build`.

## Publishing

- **Method 1: push to main:** only available to instructors with repo push access -- directly committing and pushing to `main` triggers a GitHub Action that builds and deploys automatically
- **Method 2: via pull request:** for everyone else (or when instructors are trying to be careful) -- push a branch and open a PR. The site is **built as a check on the PR** so you can confirm it compiles before merging; only merging to `main` actually deploys it

The site updates iff the build succeeds
