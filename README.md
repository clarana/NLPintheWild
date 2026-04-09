# 11-811 Course Website

Template for the CMU LTI 11-811 course website.

## Pages

| File | Description |
|------|-------------|
| `index.html` | Main page — course overview, schedule preview, grading, staff, policies |
| `schedule.html` | Full semester schedule with readings and due dates |
| `assignments.html` | Homework, paper presentation, and research project details |
| `style.css` | Shared stylesheet (responsive, CMU-branded) |

## Customization Checklist

Before deploying, replace every `[placeholder]` with real content:

- `[Course Title]` — the full course name
- `[Instructor Name]` — instructor's name (and link to faculty page)
- `[TA Name 1]` / `[TA Name 2]` — TA names
- `[Topic A]` … `[Topic F]` — actual unit/topic names
- `[Guest Speaker Name]` / `[Affiliation]` / `[Talk Title]` — guest lecture details
- `[Paper X]` / `[Author et al., Year]` — real paper titles and links
- Gradescope course code in `assignments.html`
- Office hours times and rooms
- Piazza course link
- Dates (adjust week/date column in the schedule tables)

## Deployment

This is a static HTML site — no build step required.

**GitHub Pages** (recommended):
1. Push to a GitHub repository.
2. Go to **Settings → Pages**.
3. Set the source branch to `main` (or `gh-pages`) and the folder to `/` (root).
4. Your site will be available at `https://<username>.github.io/<repo>/`.

**Local preview**:
```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
.
├── index.html        # Home page
├── schedule.html     # Full schedule
├── assignments.html  # Assignments
└── style.css         # Shared styles
```

