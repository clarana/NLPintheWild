# GitHub Pages Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up the `clarana/11811` repo as a Jekyll + Minima site deployable to `https://clarana.github.io/11811` via GitHub Pages with no Actions workflow.

**Architecture:** All Jekyll source files live at the repo root on `main`. GitHub Pages detects Jekyll automatically and builds on every push. Local preview uses the `github-pages` gem to match the deployed environment exactly.

**Tech Stack:** Jekyll, Minima theme, `github-pages` gem, Bundler, GitHub Pages (native Jekyll support)

---

### Task 1: Fix git remote URL

The repo was renamed from `11811-site` to `11811` on GitHub. The local remote still points to the old name.

**Files:**
- No files changed — git config only

- [ ] **Step 1: Verify current remote**

```bash
git remote -v
```
Expected output:
```
origin  https://github.com/clarana/11811-site.git (fetch)
origin  https://github.com/clarana/11811-site.git (push)
```

- [ ] **Step 2: Update remote URL**

```bash
git remote set-url origin https://github.com/clarana/11811.git
```

- [ ] **Step 3: Verify updated remote**

```bash
git remote -v
```
Expected output:
```
origin  https://github.com/clarana/11811.git (fetch)
origin  https://github.com/clarana/11811.git (push)
```

---

### Task 2: Create `.gitignore`

Prevent Jekyll build output and Bundler artifacts from being committed.

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Create `.gitignore`**

Create `/Users/clarana/11811-site/.gitignore` with this exact content:

```
_site/
.sass-cache/
.jekyll-cache/
.jekyll-metadata
vendor/
.bundle/
Gemfile.lock
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "Add .gitignore for Jekyll build artifacts"
```

---

### Task 3: Create `Gemfile`

Pin the `github-pages` gem so local Jekyll builds use the same gem versions as GitHub Pages.

**Files:**
- Create: `Gemfile`

- [ ] **Step 1: Create `Gemfile`**

Create `/Users/clarana/11811-site/Gemfile` with this exact content:

```ruby
source "https://rubygems.org"

gem "github-pages", group: :jekyll_plugins
```

- [ ] **Step 2: Install gems**

```bash
cd /Users/clarana/11811-site
bundle install
```

Expected: Bundler resolves and installs `github-pages` and all its dependencies (Jekyll, Minima, etc.). This will take a minute. A `Gemfile.lock` is generated but is excluded by `.gitignore`.

- [ ] **Step 3: Commit**

```bash
git add Gemfile
git commit -m "Add Gemfile pinned to github-pages gem"
```

---

### Task 4: Create `_config.yml`

Jekyll configuration: sets the site URL, baseurl, theme, and basic metadata.

**Files:**
- Create: `_config.yml`

- [ ] **Step 1: Create `_config.yml`**

Create `/Users/clarana/11811-site/_config.yml` with this exact content:

```yaml
title: "11811"
description: "Course website for 11811"
url: "https://clarana.github.io"
baseurl: "/11811"

theme: minima

# Exclude non-site files from the build
exclude:
  - docs/
  - Gemfile
  - Gemfile.lock
  - README.md
```

- [ ] **Step 2: Verify Jekyll can read the config**

```bash
cd /Users/clarana/11811-site
bundle exec jekyll doctor
```

Expected: No errors. If you see `Could not find gem 'minima'`, run `bundle install` again.

- [ ] **Step 3: Commit**

```bash
git add _config.yml
git commit -m "Add Jekyll config for GitHub Pages"
```

---

### Task 5: Create `index.md`

Homepage placeholder. Content will be filled in later — this just ensures the site builds and serves a page.

**Files:**
- Create: `index.md`

- [ ] **Step 1: Create `index.md`**

Create `/Users/clarana/11811-site/index.md` with this exact content:

```markdown
---
layout: home
---

# 11811

Course website coming soon.
```

- [ ] **Step 2: Commit**

```bash
git add index.md
git commit -m "Add homepage placeholder"
```

---

### Task 6: Create `assets/css/custom.scss`

Empty Minima style override file — establishes the pattern for future CSS customization.

**Files:**
- Create: `assets/css/custom.scss`

- [ ] **Step 1: Create the file**

```bash
mkdir -p /Users/clarana/11811-site/assets/css
```

Create `/Users/clarana/11811-site/assets/css/custom.scss` with this exact content:

```scss
---
---

// Custom styles go here. This file overrides Minima's defaults.
// Import Minima's base styles first:
@import "minima";
```

- [ ] **Step 2: Commit**

```bash
git add assets/css/custom.scss
git commit -m "Add custom.scss scaffold for Minima style overrides"
```

---

### Task 7: Verify local build

Confirm the site builds and serves locally before pushing to GitHub.

**Files:**
- No files changed

- [ ] **Step 1: Run local dev server**

```bash
cd /Users/clarana/11811-site
bundle exec jekyll serve
```

Expected output (last few lines):
```
    Server address: http://127.0.0.1:4000/11811/
  Server running... press ctrl-c to stop.
```

- [ ] **Step 2: Open in browser**

Navigate to `http://127.0.0.1:4000/11811/`

Expected: A Minima-styled page with the heading "11811" and "Course website coming soon."

- [ ] **Step 3: Stop the server**

Press `Ctrl-C` in the terminal.

---

### Task 8: Push to GitHub and enable GitHub Pages

**Files:**
- No files changed

- [ ] **Step 1: Push `main` to GitHub**

```bash
git push origin main
```

Expected: All commits pushed successfully.

- [ ] **Step 2: Enable GitHub Pages in repo settings**

1. Go to `https://github.com/clarana/11811`
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select **Deploy from a branch**
4. Set **Branch** to `main`, folder to `/ (root)`
5. Click **Save**

- [ ] **Step 3: Wait for build and verify**

GitHub will show a banner: "Your site is published at `https://clarana.github.io/11811/`"

This typically takes 1-2 minutes. Navigate to `https://clarana.github.io/11811/` to confirm the site is live and looks the same as the local preview.
