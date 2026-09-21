import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo

    import hashlib
    import io
    import json
    import pathlib
    import re
    import tempfile
    import time
    from collections import Counter, defaultdict
    from urllib.parse import unquote

    import numpy as np
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    from matplotlib import pyplot as plt


@app.cell(hide_code=True)
def _():
    mo.callout(
        mo.md(r"""
    **How this notebook works:**

    Lab 2 contains a Part I and a Part II (both in this notebook).

    - **Part I is individual.** You build one small corpus from a Wikipedia page
      that was chosen because it can be parsed, and answer Questions 1 to 3.
    - **Part II is group work, with individual writeups.** You and your project
      group point the same machinery at a source you actually mean to use, and
      each of you answers Questions 4 to 7 in your own copy.
    - Cells marked `# TODO(student)` are yours to write. Everything else runs as
      given.
    - Cells marked `[REUSABLE]` are the HTTP plumbing, in Part I. Read them
      rather than write them: Part II asks you to do the same job against your
      own source, and these are the shapes to copy.
    - Part I needs no key and no account. Its corpus is cached next to the
      notebook, so re-running it costs no requests.
    """),
        kind="info",
    )
    return


@app.cell
def _():
    # --- Fill in your info ---------------------------------------------------
    NAME = ""
    ANDREW_ID = ""
    GROUP = ""            # your project group, for Part II
    ASSIGNMENT = "Lab 2: Off-the-Shelf and Custom Pipelines for Text Analysis"
    DATE = ""             # e.g. 2026-10-01

    _missing = [
        _k for _k, _v in [("NAME", NAME), ("ANDREW_ID", ANDREW_ID), ("DATE", DATE)]
        if not _v.strip()
    ]
    _header = mo.md(
        f"# {ASSIGNMENT}\n\n**Name:** {NAME or '(name)'}\n\n"
        f"**Andrew ID:** {ANDREW_ID or 'andrewID'}\n\n"
        f"**Group:** {GROUP or '(group, for Part II)'}\n\n**Date:** {DATE or '(date)'}"
    )
    _header if not _missing else mo.vstack([
        _header,
        mo.callout(mo.md(f"Header incomplete. Fill in: {', '.join(_missing)}"), kind="warn"),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## What to hand in

    **This notebook**, with all seven questions answered, and nothing else. The
    answer sheet below tracks how many you have written.

    | | comes from | what |
    |---|---|---|
    | 1 | Part I | Questions 1 to 3, and the Part I data card |
    | 2 | Part II | Questions 4 to 7, answered for **your group's own source** rather than the worked example |
    | 3 | Part II | your blocker log and the Part II data card |

    Part I is individual work. Part II is built with your project group, but the
    notebook and the writeup you submit are your own: you should be able to
    defend every cell you hand in.

    **Do not submit any downloaded cache.** Part I ships with one, and Part II
    will build one; both stay on your machine.
    """)
    return


@app.cell
def _():
    QUESTIONS = {
        1: "Parser or API",
        2: "Which issues do you choose to deal with?",
        3: "What is still broken",
        4: "Modality and cost",
        5: "What counts as one document",
        6: "What counting revealed",
        7: "Hypothesis, result, verdict",
    }
    PLACEHOLDER = "(write your answer here)"
    return PLACEHOLDER, QUESTIONS


@app.cell(hide_code=True)
def _(ANSWERS, PLACEHOLDER, QUESTIONS):
    _rows, _done = [], 0
    for _n, _title in QUESTIONS.items():
        _a = (ANSWERS.get(_n) or "").strip()
        _ok = bool(_a) and _a != PLACEHOLDER.strip()
        _done += _ok
        _part = "Part I" if _n <= 3 else "Part II"
        _rows.append(
            f"**{'\u2705' if _ok else '\u2b1c'} Question {_n} ({_part}): {_title}**\n\n"
            + (_a if _ok else "_not yet answered_")
        )
    mo.vstack([
        mo.md(f"## Answer sheet: {_done}/{len(QUESTIONS)} written"),
        mo.callout(
            mo.md("Answers live in this notebook's code. Fill in each `answer_N` cell "
                  "below the question; re-run to refresh this sheet."),
            kind="info",
        ),
        mo.md("\n\n---\n\n".join(_rows)),
    ])
    return


@app.cell
def _(answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7):
    # marimo does not track in-place dict writes, so the registry is rebuilt here.
    ANSWERS = {1: answer_1, 2: answer_2, 3: answer_3,
               4: answer_4, 5: answer_5, 6: answer_6, 7: answer_7}
    return (ANSWERS,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Part I: one corpus, end to end

    Individual work. Questions 1 to 3.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In Lab 1 Pt 2, we downloaded and analyzed William Shakespeare's plays in XML form.
    In Lab 2, we will explore more involved ways to acquire data from the web and
    analyze it. Part 1 of Lab 2 walks you through an example that has you both parse
    a live webpage and send requests via an API to gather a corpus and conduct an
    open-ended (or self-directed) exploration of it.

    For this homework assignment, we are asking you to acquire a specific corpus
    and then come up with additional use cases for it post-hoc. This is a valid way
    of approaching a project and can lead to interesting outcomes, especially when
    there is already a general sense that the data is itself interesting in some way.
    However, for your project, you may want to (though you are not required to) start
    with a more specific agenda, and come up with a plan to acquire data to support the
    agenda vs. the other way around. The agenda may be, for example, a research question(s)
    that the data can help to answer, a downstream application that the corpus can be useful
    as training or evaluation data for, an interface that the corpus is meant to underlie.

    ### Pre-defined, open-ended question:

    > ***What kinds of multi-sport backgrounds do elite athletes have in their youth?***

    There is no single correct way to compute this-- we will work through a reasonable
    baseline, discuss judgment calls and assumptions made, and consequences thereof

    ---
    ## Corpus source and description:

    We use Wikipedia's [List of multiple Olympic gold
    medalists](https://en.wikipedia.org/wiki/List_of_multiple_Olympic_gold_medalists)
    as a reasonable starting point and proxy for "elite athlete".

    **Open the page in a browser now and scroll through it.** You will observe that it is
    not just one "list" but three:

    | Table | What it lists | Athletes |
    |---|---|---|
    | 1 | Most golds overall | 246 |
    | 2 | Progression of the all-time record | 22 |
    | 3 | Most golds at a single Games | 216 |

    There is a lot of overlap between these tables, but no table is a strict subset of another.
    We will consider the union of athletes represented across the three tables.

    ---

    ## Part I, Section 0: good practice

    As we discussed in class, there are rules we should follow when we are trying to access
    the internet via automated traffic to servers paid for by someone else.

    1. Know the license: Wikipedia text is CC BY-SA 4.0, which allows reuse with attribution and release under the same license
    2. Identify your client; send a `User-Agent` naming the tool and a contact. The policy takes an email or a website; we default to the course page so no one has to publish a personal email address, and you can swap in your own if you would rather be identifiable
    3. Read `robots.txt` first, for the paths the operator finds expensive and other explicit guidelines operators have for use. In Wikipedia's case, the `robots.txt` is [quite long and interesting](https://en.wikipedia.org/robots.txt).
    4. Go slowly, back off when told; honor `HTTP 429` and `Retry-After`
    5. Cache everything!! Re-running a cell should not require additional requests; instead, you should cache results of previous calls locally

    Section 0b implements all five, in about 90 lines. Read it -- that is the
    whole of our HTTP discipline, and Part II asks you to do the same thing
    against a source of your own choosing.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part I, Section 0b: HTTP request plumbing

    Everything below runs on these. They are short on purpose -- read all of it,
    because this is the whole of the HTTP discipline from Section 0, and Part II
    asks you to do the same thing against a source of your own choosing.

    Cells marked `[REUSABLE]` are the ones worth copying into Part II. The rest
    of this notebook is specific to Wikipedia; these three are not.
    """)
    return


@app.cell
def _():
    # [REUSABLE] Identity and throttle. Every request in this notebook goes
    # through fetch(), so the politeness rules are enforced in one place.
    #
    # CONTACT travels with every request and lands in Wikimedia's public server
    # logs. It defaults to the course page so no one has to publish a personal
    # address. *Swap in your own email or wiki username* if you would rather be
    # identifiable.\
    CONTACT = "https://nlpinthewild.clarasna.com/"
    MIN_INTERVAL = 0.25                        # seconds between requests
    API = "https://en.wikipedia.org/w/api.php"
    LIST_URL = "https://en.wikipedia.org/wiki/List_of_multiple_Olympic_gold_medalists"
    DATA = pathlib.Path("data")
    CACHE = DATA / "cache"
    CACHE.mkdir(parents=True, exist_ok=True)

    _session = requests.Session()
    _session.headers["User-Agent"] = (
        f"11811-lab2/0.1 ({CONTACT}) python-requests/{requests.__version__}"
    )
    _last = [0.0]

    def fetch(url, params=None, tries=5):
        """Return a Response, after throttling and retrying politely. Raises on 4xx."""
        delay = 1.0
        for _ in range(tries):
            _gap = time.monotonic() - _last[0]
            if _gap < MIN_INTERVAL:
                time.sleep(MIN_INTERVAL - _gap)
            _last[0] = time.monotonic()
            r = _session.get(url, params=params, timeout=60)
            # 429 means we are going too fast; 5xx means the server is unhappy.
            # Both are worth retrying. A 404 or 403 is about us, so raise now.
            if r.status_code == 429 or r.status_code >= 500:
                wait = min(float(r.headers.get("Retry-After", delay)), 120)
                print(f"  HTTP {r.status_code}; sleeping {wait:.0f}s then retrying")
                time.sleep(wait)
                delay = min(delay * 2, 60)
                continue
            r.raise_for_status()
            return r
        raise RuntimeError(f"gave up after {tries} tries: {url}")

    print("User-Agent:", _session.headers["User-Agent"])
    print(f"cache: {len(list(CACHE.glob('*.json'))):,} files in {CACHE}/")
    return API, CACHE, CONTACT, DATA, LIST_URL, fetch


@app.cell
def _(API, CACHE, fetch):
    # [REUSABLE] Cache to disk first, then the handful of API calls we need.
    # Re-running any cell below should cost zero requests.

    def _cached(key, produce):
        path = CACHE / (hashlib.sha1(key.encode()).hexdigest()[:16] + ".json")
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        value = produce()
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return value

    def get_html(url):
        """Return a page's HTML, from cache when we have already fetched it."""
        return _cached("html:" + url, lambda: fetch(url).text)

    def api_get(**params):
        """Return the MediaWiki API's JSON. Cached, except for error responses."""
        params = {**params, "format": "json", "formatversion": 2, "maxlag": 5}
        key = "api:" + json.dumps(params, sort_keys=True)
        path = CACHE / (hashlib.sha1(key.encode()).hexdigest()[:16] + ".json")
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        body = fetch(API, params).json()
        if "error" in body:
            # Caching this would make one bad request permanent.
            print("  API error, not cached:", body["error"].get("code"))
            return body
        path.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
        return body

    def get_sections(title):
        """Return an article's table of contents. No HTML, no parsing."""
        b = api_get(action="parse", page=title, prop="sections", redirects=1)
        return [] if "error" in b else b["parse"]["sections"]

    def get_extract(title):
        """Return (canonical_title, plain text). Headings survive as '== Name =='."""
        b = api_get(action="query", prop="extracts", explaintext=1,
                    redirects=1, titles=title)
        pages = b.get("query", {}).get("pages", [])
        return (pages[0].get("title"), pages[0].get("extract", "")) if pages else (None, "")

    def resolve_titles(titles, batch=40):
        """Return {requested: canonical}, following redirects. Do this before dedup."""
        out = {}
        titles = list(titles)
        for i in range(0, len(titles), batch):
            group = titles[i:i + batch]
            q = api_get(action="query", redirects=1,
                        titles="|".join(group)).get("query", {})
            norm = {x["from"]: x["to"] for x in q.get("normalized", [])}
            redir = {x["from"]: x["to"] for x in q.get("redirects", [])}
            for t in group:
                cur = norm.get(t, t)
                out[t] = redir.get(cur, cur)
        return out

    return get_extract, get_html, get_sections, resolve_titles


@app.cell
def _(DATA):
    # [REUSABLE] Turning one long string into addressable sections. Nothing here
    # is Wikipedia-specific except the '== Heading ==' convention itself.
    _HEADING = re.compile(r"^(={2,6})\s*(.+?)\s*\1\s*$", re.M)

    def split_sections(text):
        """Return [{name, level, body}]. Text before the first heading is '__lead__'."""
        out, start, name, level = [], 0, "__lead__", 1
        for m in _HEADING.finditer(text):
            out.append({"name": name, "level": level, "body": text[start:m.start()].strip()})
            start, name, level = m.end(), m.group(2), len(m.group(1))
        out.append({"name": name, "level": level, "body": text[start:].strip()})
        return out

    def take_section(spans, pattern):
        """Return (heading, text) for the FIRST matching section, plus its subsections."""
        rx = re.compile(pattern, re.I)
        for i, s in enumerate(spans):
            if not rx.search(s["name"]):
                continue
            parts = [s["body"]]
            for later in spans[i + 1:]:
                if later["level"] <= s["level"]:
                    break
                parts.append(later["body"])
            return s["name"], "\n".join(x for x in parts if x)
        return None, ""

    def load_extracts(path=None):
        """Return {title: text} from the extracts we collected for you."""
        path = path or (DATA / "olympic_extracts.jsonl")
        out = {}
        for line in open(path, encoding="utf-8"):
            r = json.loads(line)
            out[r["title"]] = r["extract"]
        return out

    return load_extracts, split_sections, take_section


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Manual checks before we build anything

    It costs just a couple manual / proof-of-concept checks to find out whether
    an athlete's Wikipedia article even often discusses their childhood sport.

    Before any scraping and before collecting any list of athletes, we read at least
    one article by hand. Run the cell below and read the output
    """)
    return


@app.cell
def _(get_extract, split_sections, take_section):
    # One athlete, one request. Does the text even discuss childhood sport?
    _title, _text = get_extract("Chris Hoy")
    _spans = split_sections(_text)
    print(f"{_title}: {len(_text.split()):,} words, {len(_spans)} sections")
    print("level-2 headings:", [_s["name"] for _s in _spans if _s["level"] == 2][:10])
    _name, _body = take_section(_spans, r"^(early|childhood|youth|background|biography)")
    print()
    print(f"matched section: {_name!r}")
    print()
    print(" ".join(_body.split())[:700])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Chris Hoy is a track cyclist. He won six Olympic golds in cycling and
    nothing else. And yet the very first paragraph of his "Early life"
    section says: *"Before track cycling, Hoy raced BMX between the ages of
    7 and 14 and was ranked second in Britain."* He also rowed for his
    school
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Acquiring a list of athletes across multiple tables

    We need every athlete from the original page, plus a link we can resolve to an
    article title later. **Open the [page](https://en.wikipedia.org/wiki/List_of_multiple_Olympic_gold_medalists)
    in a browser before you write anything** and look at the three tables.
    There are only a few row shapes here, and hardcoding what you actually see
    is fair game, but you will want to verify that you are actually grabbing what
    you are expecting you need!
    """)
    return


@app.cell
def _(LIST_URL, get_html):
    list_html = get_html(LIST_URL)
    print(f"{len(list_html):,} characters of HTML for one article.")
    print(f"'wikitable' appears {list_html.count('wikitable')} times.")

    # The one-line version: pandas.read_html finds every <table> and returns
    # DataFrames, rowspans on the rank column resolved and all.
    quick_tables = pd.read_html(io.StringIO(list_html), match="Athlete")
    print(f"\n{len(quick_tables)} tables matched. First table, head:")
    print(quick_tables[0].head(8))

    # What that one-liner throws away: look at one row before writing a parser.
    _soup = BeautifulSoup(list_html, "lxml")
    _cell = _soup.select("table.wikitable")[0].select("tr")[1].find_all(["td", "th"], recursive=False)[1]
    print("\nLinks found in one athlete cell (read_html gives us none of this):")
    for _a in _cell.find_all("a"):
        print(f"  text={_a.get_text(strip=True)!r:24s} href={_a.get('href')!r}")
    return (list_html,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 1: Parser or API

    **A selector like `a[href^="/wiki/"]`, or one that assumes the athlete is
    always in the second column, returns the wrong thing on this page. What went
    wrong, concretely? We could have reached for the API instead of
    BeautifulSoup: would it have failed the same way, and would it have gotten us
    this list at all?**

    Answer in ~3-4 sentences. Address a) one of the two broken selectors, b) what
    the API would and would not have given us here, and c) the rule you would use
    next time to choose between them. Part (c) is the one that carries over to
    Part II, so spend your words there.
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_1 = PLACEHOLDER
    mo.md(answer_1)
    return (answer_1,)


@app.cell
def _():
    def link_title(anchor):
        """Canonical article title from an <a>, or None if it is not an article link."""
        # TODO(student)
        # 1. Pull the part after /wiki/ out of the href. The hrefs on this page
        #    are absolute (https://en.wikipedia.org/wiki/...), not the
        #    root-relative /wiki/... form most tutorials still show, so an exact
        #    prefix test like href.startswith("/wiki/") matches nothing here.
        #    Search for /wiki/ anywhere in the href so it works on either form.
        # 2. Percent-decode it (unquote) and turn "_" into " ".
        # 3. Return None for non-article links. A title containing ":" is a
        #    namespace page (File:, Category:, Help:), not a person.
        raise NotImplementedError


    def span_of(cell, attr):
        """How many rows or columns a cell covers. Assumes a well-formed value."""
        return max(1, int(cell.get(attr, 1)))


    def build_grid(trs):
        """Expand a table into {(row, col): cell}, honouring rowspan AND colspan.

        Counting cells per row does not work on this page. The rank cell for
        a tied pair carries rowspan=2 and occupies the same column on the
        next row without appearing in that row's cell list, so that row comes
        up short. A naive parser either misreads the row's columns or drops
        it. Laying the table out on a grid first removes the guesswork.
        """
        grid = {}
        for r, tr in enumerate(trs):
            col = 0
            for cell in tr.find_all(["th", "td"], recursive=False):
                # Skip any column an earlier row's rowspan already filled.
                while (r, col) in grid:
                    col += 1
                rowspan = span_of(cell, "rowspan")
                colspan = span_of(cell, "colspan")
                for dr in range(rowspan):
                    for dc in range(colspan):
                        grid[(r + dr, col + dc)] = cell
                col += colspan
        return grid


    def scrape_athlete_list(html):
        """One row per athlete link, across all three wikitables on the page."""
        soup = BeautifulSoup(html, "lxml")
        content = soup.select_one("div.mw-parser-output") or soup
        rows = []

        for table_i, table in enumerate(content.select("table.wikitable")):
            # find_all("tr") is recursive, so a nested table's rows would be
            # flattened into this one. Keep only rows this table actually owns.
            trs = [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]
            if not trs:
                continue

            # TODO(student) A: lay the table out on a grid that honours BOTH
            # rowspan and colspan (build_grid above does this), then read the
            # column indices BY NAME off the grid's row 0 -- not off the list of
            # <th> elements. The two stop agreeing the moment a header cell
            # carries a colspan, and then every later column index is shifted by
            # one, silently. You want, roughly:
            #
            #   grid = build_grid(trs)
            #   if not grid: continue
            #   n_cols = 1 + max(col for (_row, col) in grid)
            #   header_at = {}   # {header text: column index}, from grid row 0
            #
            # Skip any table with no "Athlete" column: not every wikitable on a
            # page is a table of people.
            #
            # TODO(student) B: for each data row, look up that row's Athlete
            # cell on the grid and skip the row if it has none. A rowspan from
            # an earlier row can leave a later row with no cell of its own in a
            # given column, which is exactly how tied ranks are laid out here.
            #
            # TODO(student) C: append one row per article link in the Athlete
            # cell, with keys: table, sport, nation, display_name, title. Take
            # `title` from link_title(anchor) and `display_name` from
            # anchor.get_text(strip=True); read `sport` and `nation` off the
            # grid using the indices from A. Some cells hold more than one
            # athlete link (a name change, or a multi-athlete event), so do not
            # assume one link per cell.
            raise NotImplementedError

        return pd.DataFrame(rows)

    # %%
    return (scrape_athlete_list,)


@app.cell
def _(list_html, scrape_athlete_list):
    athlete_rows = scrape_athlete_list(list_html)
    print(f"link-rows scraped: {len(athlete_rows)}   distinct raw titles: {athlete_rows.title.nunique()}")
    for _t in sorted(athlete_rows.table.unique()):
        _sub = athlete_rows[athlete_rows.table == _t]
        print(f"  table {_t}: {len(_sub)} rows, {_sub.title.nunique()} distinct athletes")

    # Sanity checks. Run these before believing anything downstream: a
    # scraper that quietly skips or misaligns rows looks exactly like one
    # that worked.
    _checks = {
        # A leaked flag or nation string arrives with the WRONG title, not
        # the wrong display_name, so it lands in `title`. Checking the wrong
        # column would always pass.
        "no nation strings captured as athlete titles": "United States" not in set(athlete_rows.title),
        # Require the row to EXIST as well as look clean: .notna().all() is
        # True on an empty selection, so a dropped row would pass silently.
        "tied-rank row kept its sport (Carl Lewis, rank shared with Dressel)": (
            athlete_rows.display_name.eq("Carl Lewis").any()
            and athlete_rows.loc[athlete_rows.display_name.eq("Carl Lewis"), "sport"].notna().all()
        ),
        "a name-change row kept both links (Viktor An / Ahn Hyun-soo)": (
            {"Ahn Hyun-soo", "Viktor An"} <= set(athlete_rows.display_name)
        ),
        "a team event expanded into its individual members (1896 gymnastics)":
            "Hermann Weingärtner" in set(athlete_rows.title),
        "known athlete present": "Usain Bolt" in set(athlete_rows.title),
        "no namespace pages": not any(":" in t for t in athlete_rows.title),
    }
    for _name, _passed in _checks.items():
        print(f"  {'PASS' if _passed else 'FAIL'}  {_name}")
    athlete_rows.head(8)
    return (athlete_rows,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part I, Section 2: deduplicating athletes

    506 link-rows are not 506 athletes. **Redirects** point at a title
    that is not the article's current name, so deduplicating on the raw
    title double-counts. **Repeats**: a dominant athlete legitimately
    appears on more than one table, more than once inside the
    record-progression table, or twice in one row (two names, two
    countries). Neither is a scraping bug.
    """)
    return


@app.cell
def _(athlete_rows, resolve_titles):
    resolved = resolve_titles(sorted(athlete_rows.title.unique()))
    athlete_table = athlete_rows.assign(canonical=athlete_rows.title.map(resolved))

    _changed = {k: v for k, v in resolved.items() if k != v}
    _t0 = set(athlete_table.loc[athlete_table.table == 0, "canonical"])
    _t2 = set(athlete_table.loc[athlete_table.table == 2, "canonical"])
    _counts = athlete_table.canonical.value_counts()

    print(f"link-rows: {len(athlete_rows)}, distinct raw titles: {athlete_rows.title.nunique()}, "
          f"distinct canonical titles (union across all 3 tables): {athlete_table.canonical.nunique()}")
    print(f"\n{len(_changed)} titles changed on redirect resolution:")
    for _k, _v in _changed.items():
        print(f"  {_k!r} -> {_v!r}")
    print(f"\nin both table 1 (most golds overall) and table 3 (most golds at a single Games): "
          f"{len(_t0 & _t2)}")
    print(f"appear in more than one list row: {int((_counts > 1).sum())}")
    return (athlete_table,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Worth reading that list closely before moving on. Renames can come from
    a married name (`Ingrid Krämer` to `Ingrid Gulbin`), a transliteration
    (`Sawao Kato` to `Sawao Katō`), or a disambiguator an editor tightened
    (`Archie Hahn (athlete)` to `Archie Hahn (sprinter)`). However, two of
    the eleven are not renames at all: `Konrad Böcker` to `Conrad Böcker`
    and `Georg Hilmar` to `Georg Hillmar` fix a misspelling in the list's
    own link text.

    A title is a label editors chose, not a stable identifier. Follow the redirect
    graph to make sure that you arrive at the current canonical page for a
    person.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part I, Section 3: per-article biographies via API

    For 362 people we want one article each. Compare scraping (362 fetches
    of half a megabyte or more of HTML each, then a parser that survives
    every biography's layout) against the API: `action=parse&prop=sections`
    returns headings with nesting level, no parsing needed;
    `action=query&prop=extracts&explaintext=1` returns plain text with
    headings kept as `== Heading ==`, no markup, no reference markers, no
    infobox debris.
    """)
    return


@app.cell
def _(get_sections):
    _sections = get_sections("Michael Phelps")
    _top = [_s for _s in _sections if _s["level"] == "2"]
    print(f"{len(_sections)} sections in all, {len(_top)} of them top-level:")
    for _s in _top:
        print(f"  [{_s['index']:>2}] {_s['line']}")
    return


@app.cell
def _(API, athlete_table, fetch, load_extracts):
    import random as _random

    athletes = sorted(athlete_table.canonical.unique())
    texts = load_extracts()

    # Is the cache we shipped you still what Wikipedia says? Checking that has to
    # go around our own cache. Calling get_extract here would hand back the very
    # file we are trying to check, and the test would pass no matter what.
    _probe = _random.Random(11811).sample(athletes, 3)
    _match = _reached = 0
    for _t in _probe:
        try:
            _live = fetch(API, {"action": "query", "prop": "extracts", "explaintext": 1,
                                "redirects": 1, "titles": _t, "format": "json",
                                "formatversion": 2, "maxlag": 5}).json()
            _body = _live["query"]["pages"][0].get("extract", "")
        except Exception as _e:
            print(f"  could not reach Wikipedia for {_t!r} ({type(_e).__name__})")
            continue
        _reached += 1
        _match += _body == texts.get(_t)

    if _reached == 0:
        print(f"{len(texts):,} cached extracts. Could not reach Wikipedia, so the "
              f"cache is unchecked. Everything below still runs.")
    else:
        print(f"{len(texts):,} cached extracts; {_match} of {_reached} still match "
              f"Wikipedia word for word today.")
        if _match < _reached:
            print("  A mismatch is drift, not a bug. These articles get edited daily,")
            print("  which is the reason we shipped a cache instead of a live fetch.")

    _wc = np.array([len(t.split()) for t in texts.values()])
    _p10, _median, _p90 = (int(x) for x in np.percentile(_wc, [10, 50, 90], method="averaged_inverted_cdf"))
    _under500 = int((_wc < 500).sum())
    print(f"\nn = {len(_wc)} articles, median {_median:,} words, p10 {_p10:,}, p90 {_p90:,}, "
          f"max {int(_wc.max()):,}, under 500 words: {_under500} ({round(100 * _under500 / len(_wc))}%)")
    return athletes, texts


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part I, Section 4: finding the childhood material

    `split_sections` above gives `{"name", "level", "body"}` spans;
    `take_section` pulls the first section whose heading matches a regex,
    with subsections included. Wikipedia pages for people do not follow
    universal structures. This means that childhood info may or may not
    have its own structure, and it might be located under a variety of
    headers. We picked out a few as plausible names for sections
    containing early life material
    """)
    return


@app.cell
def _(athletes, split_sections, take_section, texts):
    spans_by_person = {t: split_sections(texts[t]) for t in athletes if t in texts}

    _terms = ["early", "personal life", "biography", "background", "childhood", "youth"]

    def _starts_with(spans, term):
        return bool(take_section(spans, r"^" + term)[0])

    _per_doc = {t: {term: _starts_with(s, term) for term in _terms} for t, s in spans_by_person.items()}

    _rows = []
    for _term in _terms:
        _total = sum(1 for _d in _per_doc.values() if _d[_term])
        _unique = sum(
            1 for _d in _per_doc.values()
            if _d[_term] and sum(_d[_other] for _other in _terms if _other != _term) == 0
        )
        _rows.append({"term": _term, "articles with such a section": _total, "unique to this term": _unique})
    term_table = pd.DataFrame(_rows).sort_values("articles with such a section", ascending=False)
    term_table
    return (spans_by_person,)


@app.cell
def _(spans_by_person, take_section):
    _n = len(spans_by_person)
    _exact = sum(1 for _s in spans_by_person.values() if take_section(_s, r"^early life$")[0])
    _pct = 100 * _exact / _n

    print(f"heading is exactly 'Early life' in only {_exact} of {_n} ({_pct:.1f}%)")
    print()
    print("The style guide made 'Early life' the convention, so it is tempting to")
    print("scope the corpus to that heading and move on. However, older articles, ")
    print("and articles not primarily in English, might have similar information ")
    print("under 'Personal life' or 'Biograph' or some other non-standard article ")
    print("title. Stubs often lack meaningful headings at all.")
    return


@app.cell
def _(athletes, spans_by_person, take_section):
    EARLY_LIFE_PATTERN = r"early life"
    # TODO(student): decide whether to widen beyond `early life`, and to what.
    # The per-term table above is your evidence. Each row shows how many
    # articles a candidate term would add, and how many of those no other term
    # reaches ("unique to this term"). Build BACKFILL_PATTERN as a regex
    # alternation from terms that earn their place on that table. Adding a term
    # costs you something: Question 2 asks what.
    BACKFILL_PATTERN = r"early life"   # TODO: widen this, or argue for leaving it

    early_life, childhood = {}, {}
    for _t, _s in spans_by_person.items():
        _h, _b = take_section(_s, EARLY_LIFE_PATTERN)
        if _h and len(_b.split()) >= 40:
            early_life[_t] = _b
        _h2, _b2 = take_section(_s, BACKFILL_PATTERN)
        if _h2 and len(_b2.split()) >= 40:
            childhood[_t] = _b2

    print(f"'early life' only: {len(early_life)} of {len(athletes)} athletes "
          f"({round(100 * len(early_life) / len(athletes))}%)")
    print(f"'early life' + biography + personal life: {len(childhood)} of {len(athletes)} athletes "
          f"({round(100 * len(childhood) / len(athletes))}%)")
    return childhood, early_life


@app.cell
def _(athlete_table, childhood):
    # Who is missing? Not a random 43% of the athletes. Coverage below is the
    # share of each sport's medalists whose article gives us a usable childhood
    # section. An athlete who medalled in two sports counts once under each, so
    # these athlete counts add up to more than 362.
    _tot, _cov = {}, {}
    for _canon, _grp in athlete_table.groupby("canonical"):
        for _sp in {_p.strip() for _v in _grp.sport.dropna()
                    for _p in str(_v).split(",") if _p.strip()}:
            _tot[_sp] = _tot.get(_sp, 0) + 1
            _cov[_sp] = _cov.get(_sp, 0) + (_canon in childhood)

    coverage_by_sport = pd.DataFrame(
        [{"medal sport": _sp, "athletes": _tot[_sp], "usable section": _cov[_sp],
          "coverage %": round(100 * _cov[_sp] / _tot[_sp], 1)}
         for _sp in _tot if _tot[_sp] >= 7]
    ).sort_values("coverage %", ascending=False).reset_index(drop=True)

    print(f"coverage by medal sport, for the {len(coverage_by_sport)} sports with "
          f"at least 7 medalists:\n")
    print(coverage_by_sport.to_string(index=False))
    print(f"\nbest {coverage_by_sport['coverage %'].iloc[0]}%, "
          f"worst {coverage_by_sport['coverage %'].iloc[-1]}%. If articles went "
          f"missing at random these would all sit near "
          f"{round(100 * len(childhood) / athlete_table.canonical.nunique())}%.")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 2: Which issues do you choose to deal with?

    Adding `biography` to the pattern brings in 52 articles no other heading
    reaches, and roughly 40% of `Biography` sections have no childhood material
    in them. **Which of those two type of issues would you rather have in your data?**
    And of the 362 athletes, 155 (43%) end up with no usable section under the
    headings we picked: are those 155 missing at random?

    Answer in ~5-6 sentences. Address a) which error you would prefer to have (feel
    free to ground your answer in a specific analysis you are interested in),
    b) whether those 155 look random to you, pointing at specific numbers in
    the coverage output rather than at what sounds plausible, and c) what your answer
    to (b) does to a sentence like "N% of elite athletes played another sport as
    children". You should address all three, but they do not need equal depth:
    (b) and (c) are worth more of your time than (a).

    Some ideas and examples to get you started: "I would rather \_\_\_\_\_,
    because a corpus that \_\_\_\_\_ is easier to defend than one that
    \_\_\_\_\_" or "coverage is \_\_\_\_\_% for \_\_\_\_\_ but only
    \_\_\_\_\_% for \_\_\_\_\_, and those two differ in \_\_\_\_\_" or
    "the sentence would really mean \_\_\_\_\_, which is a claim about
    \_\_\_\_\_ rather than about athletes"
    """)
    return


@app.cell
def _(spans_by_person, take_section):
    # Heading coverage before the 40-word filter, so you can see how much of the
    # loss is "no such heading" and how much is "the heading is there but short".
    EARLY_STYLE = r"^(early|childhood|youth|background|biography)"
    PERSONAL = r"personal life"
    has_early = sum(1 for _s in spans_by_person.values() if take_section(_s, EARLY_STYLE)[0])
    has_personal = sum(1 for _s in spans_by_person.values() if take_section(_s, PERSONAL)[0])
    has_either = sum(
        1 for _s in spans_by_person.values()
        if take_section(_s, EARLY_STYLE)[0] or take_section(_s, PERSONAL)[0]
    )
    _n = len(spans_by_person)
    print(f"of {_n} athletes, by heading alone:")
    print(f"  an early-life-style heading : {has_early:>3} ({round(100*has_early/_n)}%)")
    print(f"  a 'personal life' heading   : {has_personal:>3} ({round(100*has_personal/_n)}%)")
    print(f"  either of those             : {has_either:>3} ({round(100*has_either/_n)}%)")
    print(f"  neither                     : {_n-has_either:>3} ({round(100*(_n-has_either)/_n)}%)")
    return


@app.cell
def _(PLACEHOLDER):
    answer_2 = PLACEHOLDER
    mo.md(answer_2)
    return (answer_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## The plan for the analysis

    Once we have a corpus, "find multi-sport backgrounds" is still not
    something a computer can do on its own. Here are examples of how we
    could turn it into something computable, in three passes of increasing
    effort. You are not expected to finish all three by hand; the point is
    to see why each pass exists.

    **Pass 1: decide what counts.** Write the definition down before writing
    any code. At least four different things could qualify, and they are not
    the same claim:

    | Pattern | Example |
    |---|---|
    | Switched sports before the medal sport | Chris Hoy rowed and raced BMX before track cycling |
    | Competed in two sports concurrently | Summer McIntosh: swimming and figure skating |
    | Played several sports casually in childhood | Dara Torres: basketball, gymnastics, volleyball |
    | Medalled in more than one Olympic sport | Ester Ledecká: gold in both snowboarding and alpine skiing at the 2018 Games |

    Pick one, or rank them, before you measure anything. A result that mixes
    all four silently is not a result.

    **Pass 2: a cheap first measurement.** We already know, from the list
    itself, which sport each athlete won their medals in. So instead of
    hunting for particular grammar ("switched from... to...", "also played"),
    we extract *every* sport mentioned anywhere in an athlete's childhood
    section and compare that set against their medal sport. Anything
    mentioned that is not the medal sport is a candidate multi-sport
    background. This will overcount, for reasons we measure directly in
    Section 5, but it gives us a number and a denominator to start from.

    **Pass 3: measure your own precision.** Take a random sample of the
    athletes flagged as mentioning another sport, read them by hand, and
    classify each one: did the athlete really play it, did a relative play
    it (or coach it), or is it a substring or entity match error? Use a
    sample of at least 20 athletes!

    Note: At this point, you can say what share of these articles *mention*
    a second (or third) sport. Without more work you cannot yet say what
    share of these athletes *played* one.
    """)
    return


@app.cell
def _():
    # Section 5: the multi-sport analysis.
    SPORT_WORDS = {
        # "track" on its own is not in this list on purpose. It matches "short
        # track", "skiing track" and "Konigssee track", none of which are
        # athletics. Word boundaries do not help here, since every one of those
        # is the whole word "track". Phrases are what separate them.
        "Athletics": ["athletics", "track and field", "track & field", "ran track",
                      "track coach", "track star", "track athlete", "track meet",
                      "sprinter", "marathon", "javelin",
                      "high jump", "long jump", "triple jump", "pole vault", "discus", "shot put",
                      "hurdles", "hurdler", "decathlon", "heptathlon", "middle-distance", "race walking"],
        "Swimming": ["swimming", "swimmer", "swimmers", "swim team", "swim club", "swim coach",
                     "swim group", "swim school"],
        # TODO(student): add an entry for every other sport that appears as
        # a `sport` value in the athlete list. Two rules, both learned the
        # hard way above: give each sport its real synonyms, and prefer a
        # PHRASE to a bare word wherever the bare word means other things
        # too (see the note on "track").
    }

    SPORT_RE = {
        _name: re.compile(r"\b(?:" + "|".join(re.escape(w) for w in sorted(_words, key=len, reverse=True)) + r")\b", re.I)
        for _name, _words in SPORT_WORDS.items()
    }
    # Entity/negation fixes: a co-ed "swimming and diving" program, "could
    # not sing or dance" (negation), "forming a football team" (an adult
    # organiser) are none of them the athlete playing the sport.
    SPORT_RE["Diving"] = re.compile(r"\b(?:diver|(?<!swimming and )diving)\b", re.I)
    SPORT_RE["Dance"] = re.compile(r"\b(?:ballet|dancer|(?<!not sing or )dance|(?<!not sing or )dancing)\b", re.I)
    SPORT_RE["Football"] = re.compile(r"\b(?:soccer|(?<!forming a )football)\b", re.I)
    return (SPORT_RE,)


@app.cell
def _(SPORT_RE, athlete_table, childhood):
    # Medal sport can be comma-joined (Ledecká); split and strip.
    medal_sports = {}
    for _canon, _grp in athlete_table.groupby("canonical"):
        _toks = set()
        for _s in _grp.sport.dropna():
            for _tok in _s.split(","):
                _tok = _tok.strip()
                if _tok:
                    _toks.add(_tok)
        medal_sports[_canon] = _toks

    print("5 athletes, mentions vs. medal sport:")
    for _t in sorted(childhood)[:5]:
        _mentioned = {n for n, rx in SPORT_RE.items() if rx.search(childhood[_t])}
        print(f"  {_t:22s} medal {medal_sports.get(_t)} found {_mentioned}")

    # Every alternative in SPORT_RE is \b-wrapped, because an unanchored
    # substring matches inside other words: "rowing" hits "growing up" and
    # "discus-throwing", which is how Rowing picks up athletes who never rowed.
    _loose = sum(1 for _b in childhood.values() if re.search(r"rowing", _b, re.I))
    _tight = sum(1 for _b in childhood.values() if re.search(r"\browing\b", _b, re.I))
    print(f"\n'rowing' as a substring: {_loose} athletes; as a whole word: {_tight}")
    return (medal_sports,)


@app.cell
def _(SPORT_RE, childhood, early_life, medal_sports):
    def _rate(corpus):
        _own = _a1 = _a2 = 0
        for _t, _body in corpus.items():
            _mentioned = {n for n, rx in SPORT_RE.items() if rx.search(_body)}
            _medals = medal_sports.get(_t, set())
            _own += bool(_mentioned & _medals)
            _others = len(_mentioned - _medals)
            _a1 += _others >= 1
            _a2 += _others >= 2
        return len(corpus), _own, _a1, _a2

    multi_n, multi_own, multi_a1, multi_a2 = _rate(childhood)
    early_n, early_own, early_a1, early_a2 = _rate(early_life)
    print(f"of {multi_n} ARTICLES with a usable childhood section: "
          f"names own medal sport {multi_own} ({round(100*multi_own/multi_n)}%), "
          f"names at least one other sport {multi_a1} ({round(100*multi_a1/multi_n)}%), "
          f"names two or more others {multi_a2} ({round(100*multi_a2/multi_n)}%)")
    print(f"on the stricter {early_n}-article 'early life'-only corpus: "
          f"{early_a1} ({round(100*early_a1/early_n)}%), about "
          f"{abs(round(100*early_a1/early_n) - round(100*multi_a1/multi_n))} points apart")

    FAMILY_RE = re.compile(
        r"\b(father|mother|dad|mom|brother|sister|sibling|parents|parent|uncle|aunt"
        r"|grandfather|grandmother|son|daughter|husband|wife"
        # A partner is not family by blood, but the sport is just as much
        # somebody else's. Sven Kramer's section names his partner's sport.
        r"|partner|girlfriend|boyfriend|fiancee|fiance|spouse)\b", re.I)

    def _sentences(text):
        return re.split(r"(?<=[.!?])\s+", text)

    family_total = family_flagged = 0
    for _t, _body in childhood.items():
        _others = {n for n, rx in SPORT_RE.items() if rx.search(_body)} - medal_sports.get(_t, set())
        for _sent in _sentences(_body):
            if any(SPORT_RE[n].search(_sent) for n in _others):
                family_total += 1
                family_flagged += bool(FAMILY_RE.search(_sent))
    print(f"of {family_total} SENTENCES flagging a non-medal sport, {family_flagged} "
          f"({round(100*family_flagged/family_total)}%) also name a family member")

    # That share is per sentence. What it costs the per-article rate is smaller:
    # only articles whose *only* evidence sits in such a sentence would flip.
    family_only_articles = 0
    for _t, _body in childhood.items():
        _others = {n for n, rx in SPORT_RE.items() if rx.search(_body)} - medal_sports.get(_t, set())
        if not _others:
            continue
        _kept = " ".join(_s for _s in _sentences(_body) if not FAMILY_RE.search(_s))
        if not ({n for n, rx in SPORT_RE.items() if rx.search(_kept)} - medal_sports.get(_t, set())):
            family_only_articles += 1
    print(f"but only {family_only_articles} of the {multi_a1} flagged ARTICLES rest on such a "
          f"sentence alone: even if every one were a relative's sport, the rate falls "
          f"{round(100*multi_a1/multi_n)}% -> {round(100*(multi_a1-family_only_articles)/multi_n)}%")
    return family_flagged, family_total, multi_a1, multi_n


@app.cell(hide_code=True)
def _(athletes, family_flagged, family_total, multi_a1, multi_n):
    mo.md(rf"""
    ### Question 3: What is still broken

    The rate in question is the **{multi_a1} of {multi_n}
    ({round(100*multi_a1/multi_n)}%)** above: articles whose childhood section
    names at least one sport outside that athlete's own medal sports. Mind the
    unit. It counts articles, not athletes, and those {multi_n} are themselves
    only {round(100*multi_n/len(athletes))}% of our {len(athletes)}.

    The {round(100*family_flagged/family_total)}% is one failure mode we happened
    to measure, and it is counted per sentence rather than per article: the
    sentence names a sport, but a relative or a partner played it, not the
    athlete. There are others, and the cell above finds none of them.

    **What failure modes are still in there? Which of them would overcount multi-sport
    experiences, and which of them undercount? Which direction do you think would
    be more damaging? How might you check whether you are right?**

    Answer in ~5-6 sentences.

    Some ideas and examples to get you started: "\_\_\_\_\_ pushes the match rate up,
    because our matcher reads \_\_\_\_\_ as participation" or "a sport word can
    turn up inside a \_\_\_\_\_, which is not a sport at all" or "the
    \_\_\_\_\_ side has to be the bigger one, because it is capped by
    \_\_\_\_\_ while the other is not" or "I would check it by \_\_\_\_\_,
    which would take about \_\_\_\_\_"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_3 = PLACEHOLDER
    mo.md(answer_3)
    return (answer_3,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part I, Section 6: the data card

    Every corpus gets one of these. A reader who never saw your code should
    be able to tell, from the card alone, what your numbers are numbers
    *of*, and what they cannot be used for. "Unknown, because ..." is
    acceptable; a blank is not.
    """)
    return


@app.cell
def _(LIST_URL, athletes, childhood):
    data_card = {
        "name": "Olympic multiple-gold-medalist childhood sections (English Wikipedia)",
        "source_list_url": LIST_URL,
        "snapshot_date": "2026-09-21 (cache); live sample re-checked at run time",
        "licence": "CC BY-SA 4.0, attribute English Wikipedia, share alike",
        "document_unit": "one childhood section per athlete: primary 'Early life', "
            "backfill 'Biography' or 'Personal life' (subsections included)",
        "childhood_definition": "heading matching r'early life|biography|personal "
            "life', at least 40 words; 102 of 207 come from 'early life' alone",
        "n_documents": len(childhood),
        "coverage": f"{len(childhood)}/{len(athletes)} athletes "
            f"({round(100 * len(childhood) / len(athletes))}%)",
        "personal_data": "third-party emails in the source text were replaced with "
            "[email-redacted] before shipping: public in their original setting, "
            "but a bundled list is a different exposure.",
        "known_biases": "population is the union of three editor-curated rankings "
            "of the same medal record, not a random sample; missingness is NOT "
            "random and skews against sports with less anglophone media coverage "
            "(rowing, wrestling, fencing, cross-country skiing vs. swimming, "
            "athletics, basketball)",
        "do_not_use_for": "any claim about what share of athletes actually played "
            "a second sport. The corpus supports claims about what Wikipedia SAYS, "
            "only for the 57% of athletes whose article says enough to check.",
    }
    mo.md(
        "**Data card**\n\n"
        + "\n".join(f"- **{_k}**: {_v}" for _k, _v in data_card.items())
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    One takeaway from Part I:

    > Use the API when it returns the object you want as data; parse the
    > markup when the structure you want exists only in the markup.

    From here, you and your project group point can point helper functions from above
    at another source you actually intend to use.

    The three `[REUSABLE]` cells from Part I are reference implementation for
    the fetch skeleton you are about to write. Scroll back to them when you need
    them; they are still live in this notebook.

    Questions 4 to 7 are below.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part II: project data proof of concept

    Part I built one small corpus end to end from a single Wikipedia page,
    chosen because it was parseable. It is easy to set up the problem to be
    more challenging. For example, looking at [this page](https://en.wikipedia.org/wiki/List_of_sports_figures_considered_the_greatest)
    instead of the multiple Olympic golds article would make the initial
    single-article parsing work much more difficult. In Part II you and your
    project group will take **the source you actually mean to use for your
    course project** and build the first working slice of a pipeline against it.

    This is a **proof of concept**, not a finished dataset. The goal is to
    build and test each *piece* of the pipeline (fetch, extract, structure,
    sample-check) against your real, messy source, and document where it
    fought back. A group that hits a real wall and documents it clearly
    scores as well as one whose source behaved perfectly: we will assess
    the rigor of what you found, not how clean the corpus turned out.

    ---
    ## Part II, Section 0: choose your data source(s)

    ### Bring your own data

    Use the source your group intends to use for the project. That is what this
    lab is for, and every cell below is written to run against whatever you pick
    rather than against a fixed dataset. A source you will still be opening in
    October is worth more here than one that is easy this week.

    Pick a source that: is available digitally now, will yield enough documents
    once you pick a unit (see Section 2 below), has a license permitting classroom
    research use, contains text extractable with ordinary tools, and is data your group
    finds interesting.

    ### If your group does not have a source yet

    We strongly encourage you to take the time to consider what dataset(s) you might
    actually want to work with for your project. That being said, we scouted four
    example data sources as fallbacks so that nobody is blocked on this step. Each
    is documented below.

    ### Lab 2 Part 2 is Group Work! (Individual reports and submissions)

    Sections 1-4 of Part 2 are group work: choose the source and build the pipeline
    together. **The notebook and the writeup you hand in are your own.** You
    should be able to defend every cell you submit, which is hard to do for code
    you watched someone else write.

    Please attempt this work without AI coding assistance. For a Post-Lab 2 activity
    we will ask you to reflect on an AI coding assistant's performance on the same task.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Fallback dataset details

    Already probed and measured once, so you know roughly what each costs
    before committing an afternoon to it. Skip this section entirely if you
    brought your own source.

    | Source | Access | Scale | What it will teach you | Known gotchas |
    |---|---|---|---|---|
    | GitHub + PyTorch topic | Auth REST (PAT). 5,000/hr core, 30/min search, 60/hr unauth | 1,277 repos match. We took the top 60 by stars (min 11,867, the top 4.7%). 60/60 READMEs | Endpoint-specific quotas, license auditing, sampling bias | 13/60 no determinable license. 11/60 also tagged `tensorflow` |
    | NeurIPS 2024 paper checklists | No key. S2 search 429s, S2 bulk does not. Proceedings want a 5-10s delay | 4,544 S2 records. 4,034 proceedings. Our cache 400, of which 396 have a checklist | Joining two sources on title, self-reported data | S2 has metadata, no PDFs (1.6% `openAccessPdf.url`). arXiv carries the checklist only 3/8 |
    | SEC EDGAR 10-K risk factors | No key. Fair access wants a contact UA and <=10 req/s | 10,438 companies. Of 30 sampled: 16 extract cleanly under the better rule; the naive rule reported 8 and only 6 held up | Section-boundary regex, repeated headings, extraction strategy | `Item 1A` appears 1-6x per filing. 11/30 filed no recent 10-K |
    | ACL Anthology | No `robots.txt`. Use the bulk-metadata route, not crawling | 131,040 entries, 1952-2026, 469 venues | ID-scheme ambiguity, metadata/PDF divergence, sampling weights | Two incompatible ID schemes. 93.2% era-balanced probe rate against 98.9% corpus-weighted |

    Each row is expanded below.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **GitHub repos using PyTorch.** A documented, authenticated API matches the
    query exactly: 1,277 repos for `topic:pytorch stars:>500 language:python`.

    GitHub meters endpoints separately, and the search quota is the one that
    binds:

    - core requests, with a token: 5,000/hour
    - search, with a token: 30/minute
    - unauthenticated: 60/hour

    We pulled the top 60 repos by star count (`sort=stars`, descending). The
    60th repo has 11,867 stars. Those 60 are the most-starred 4.7% of the
    1,277 matches, not a random sample of them. That skew matters, because
    README length and license quality both tend to correlate with popularity.

    The pull got 60/60 READMEs, median 1,539 words. Approximate p10 579, p90
    4,493. All three figures are index positions over 60 sorted values --
    `ws[n//2]`, `ws[n//10]` and `ws[9*n//10]` -- so they are really the
    51.7th, 11.7th and 91.7th percentiles. Averaging the two central values
    instead gives 1,538 words, so read the median as 1,538-1,539 depending on
    convention.

    License field over all 60 repos:

    | License | Repos |
    |---|---|
    | Apache-2.0 | 19 |
    | MIT | 19 |
    | NOASSERTION | 12 |
    | AGPL-3.0 | 4 |
    | GPL-3.0 | 2 |
    | MPL-2.0 | 1 |
    | BSD-3-Clause | 1 |
    | CC-BY-SA-4.0 | 1 |
    | null (field absent) | 1 |

    13 of the 60 have no determinable license: the 12 NOASSERTION plus the 1
    null. Those 13 become a problem the moment you redistribute.

    11/60 of these `pytorch`-tagged repos are also tagged `tensorflow`.
    Topics are self-reported, so you measure what maintainers wrote, not what
    the code imports.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **NeurIPS paper checklists.** No API key needed, but the path to the
    text is not obvious. Two sources index the same conference
    independently:

    - S2 bulk search: 4,544 records
    - the proceedings site: 4,034 papers

    S2 gives metadata, not PDFs. `openAccessPdf.url` is populated for only
    1.6% of records (16/1,000 checked). arXiv does not save you either: the
    checklist rides along only 3/8 spot-checked times (37.5%), because it is
    added at camera-ready. Proceedings PDFs carry it 99.0% of the time.

    So the design is S2 for metadata, proceedings for PDF text, joined on
    title. A DOI join is not possible: the proceedings index carries no DOI
    field at all, even though S2 does list a DOI for 4,394/4,544 records
    (96.7%). That design is worked end to end below, offline.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **SEC EDGAR 10-K risk factors.** No key. `sec.gov/robots.txt` explicitly
    *allows* `/Archives/edgar/data`, and fair access asks for a contact
    User-Agent and <=10 req/s. 10,438 companies are listed.

    The extraction is the hard part. "Item 1A" appears 1 to 6 times per
    filing (contents, cross-references, body), so which occurrence you keep
    decides what you get. We sampled 30 companies and tried two rules.

    Naive rule, pair the LAST occurrence with the next end marker:

    - 8/30 reported as a clean extraction
    - 2 of those 8 fail the same 1,000-word standard used below: `DGX` at 419
      words and `LQDA` at 540 words
    - so 6/30 were genuinely clean
    - 9/30 had no usable end marker
    - 11/30 had filed no recent 10-K at all

    Better rule, consider EVERY occurrence, pair each with its next end
    marker, keep the LONGEST span, and require at least 1,000 words:

    - 16/30 clean
    - 3/30 implausibly short
    - the same 11/30 with no recent 10-K

    19 of the 30 companies actually file a 10-K, and 16 of those 19 extract
    cleanly. `LQDA` is the clearest case. The naive rule grabbed a 540-word
    cross-reference, never clean by the 1,000-word standard. The longest-span
    rule found the real section at 40,035 words.

    Across the 16 clean extractions under the better rule, risk-factor length
    runs a median of 21,115 words (min 6,312, max 50,629; n is too small for
    percentiles) and the filing HTML a median of 2.41 MB.

    What broke here was the extraction strategy. The source data was fine.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **ACL Anthology papers.** The hardest row, and the best one for surfacing
    blockers. Neither `aclanthology.org` nor `www` serves a `robots.txt`, but
    a documented bulk-metadata route exists (the `acl-org/acl-anthology` repo
    and PyPI package). Use that, not crawling. The bulk `.bib` is 12.6 MB
    gzipped: 131,040 entries, 1952-2026, 469 venues.

    Measured gotchas:

    - Two incompatible ID schemes: 76,920 modern, like `2020.acl-1.12`, and
      54,120 legacy, like `P18-1023`. You cannot infer the scheme from the
      year, since anything ingested after 2020 was renumbered regardless of
      age.
    - 22 legacy prefixes, every one of which overlaps another one in year
      span.
    - The official docs contradict themselves on what `2020.acl-1.12` is
      called.
    - Every URL carries a trailing slash the docs do not show.

    We probed 838 PDF URLs, sampled evenly across eras rather than in
    proportion to the corpus. 93.2% resolve. That is an era-balanced probe
    rate, not a corpus rate: 1952-1969 is only 0.4% of the corpus but was
    16.2% of the probe's rows.

    | Era | Resolve rate | Share of corpus |
    |---|---|---|
    | 1950s-60s | 75.7% | 0.4% |
    | 1970s | 91.6% | 0.4% |
    | 1980s | 99.3% | 1.9% |
    | 1990s | 99.0% | 4.7% |
    | 2000s | 92.1% | 12.1% |
    | 2010s | 100.0% | 27.4% |
    | 2020s | 100.0% | 53.2% |

    Reweight those per-era rates by corpus share and you get 98.9%. A student
    sampling modern ACL papers should budget about 99% resolve, not 93%.

    DOI coverage collapses the same way, from 73.7% in the 2020s to 0% before 1970.
    Licensing splits at 2016: CC BY-NC-SA 3.0 before, CC BY 4.0 after.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Feel free to take inspiration from any of these even if your group is creating its own dataset
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part II, Section 1: acquisition

    Whatever your source, the first pipeline piece is the same fetch
    discipline as Part I, generalized: a **polite** User-Agent naming your
    tool and a contact; a **cache** so re-running costs zero new requests;
    **retry with backoff** on 429 and 5xx; and, new this time,
    **resumability** -- a 250-item fetch that dies halfway should resume, not
    restart, when you re-run it.

    Part I's three `[REUSABLE]` cells are a reference implementation of the
    first three, against one API. Adapt their shape, do not copy them blindly:
    your source's auth and error codes will differ. The skeleton below generalizes all
    four jobs, then proves retry and resume work offline, against a fake
    server.
    """)
    return


@app.cell
def _(CONTACT, Path):
    def cache_path(cache_dir, url, params=None):
        """Same url+params -> same file. RESUMABLE: check this before the network."""
        # TODO(student): hash url+params (e.g. hashlib.sha1 on a sorted-JSON
        # key) into a deterministic filename inside cache_dir. Part I's
        # _cached() has the pattern to adapt.
        raise NotImplementedError


    def polite_get(session, url, params=None, cache_dir=Path("part2_cache"),
                    contact=CONTACT, min_interval=1.0, max_tries=6, _last_call=[0.0]):
        """RESUME, IDENTIFY, THROTTLE/BACK OFF, CACHE -- the four jobs
        described above. Adapt this, do not reuse as-is: your real API
        likely needs auth headers or different pagination."""
        # TODO(student):
        #   1. RESUME: if cache_path(...) already exists, load and return its
        #      cached body -- touching the network zero times.
        #   2. THROTTLE: wait at least min_interval since the last request.
        #   3. IDENTIFY: send a User-Agent naming the tool and `contact`.
        #   4. BACK OFF: on HTTP 429 or 5xx, sleep (honour Retry-After if
        #      present) and retry with exponential backoff, up to max_tries.
        #   5. CACHE: write a successful response to disk before returning it.
        # Part I's fetch/get_html/api_get are a worked reference against one
        # specific API -- adapt their shape, do not copy them blindly.
        raise NotImplementedError

    return (polite_get,)


@app.cell
def _(Path, polite_get):
    # Proof, offline: a fake session standing in for requests. Session,
    # failing twice with 429 then succeeding. Run this once your polite_get
    # above is filled in; it should print 3 attempts then 0 new attempts.
    from types import SimpleNamespace as _NS

    def _raise(code):
        def _r():
            if code >= 400:
                raise RuntimeError(f"HTTP {code}")
        return _r

    class _FlakySession:
        n_calls = 0

        def get(self, url, params=None, headers=None, timeout=None):
            self.n_calls += 1
            if self.n_calls <= 2:
                return _NS(status_code=429, headers={"Retry-After": "0.05"}, raise_for_status=_raise(429))
            return _NS(status_code=200, text="the actual payload", headers={}, raise_for_status=_raise(200))


    _demo_dir = Path(tempfile.mkdtemp())
    _flaky = _FlakySession()

    _result_1 = polite_get(_flaky, "https://example.org/item/1", cache_dir=_demo_dir, min_interval=0.0)
    print(f"first call: {_flaky.n_calls} attempts (2 retries then success), got {_result_1!r}")

    _calls_before = _flaky.n_calls
    _result_2 = polite_get(_flaky, "https://example.org/item/1", cache_dir=_demo_dir, min_interval=0.0)
    print(f"restart-simulating second call: {_flaky.n_calls - _calls_before} new attempts, "
          f"got {_result_2!r} (from cache)")
    return


@app.cell
def _():
    # TODO(student): load what you already fetched for YOUR source. This is
    # the moment to point at YOUR cache directory, not part2_data/ (that is
    # the instructor's shipped cache for the menu rows, used only in the
    # solutions notebook's worked example).
    #
    # One reasonable shape is a list of dicts, one per document, e.g.
    #   records = [{"id": ..., "raw": ..., ...}, ...]
    # Everything below assumes a variable named `records` in roughly this
    # shape; adapt downstream cells if your data is naturally a DataFrame,
    # a directory of files, or something else instead. If you have fewer
    # than a few dozen records so far, that is fine for a proof of concept;
    # say so honestly in Question 4 rather than padding the count.
    records = []
    print(f"loaded {len(records)} records")
    return (records,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 4: Modality and cost

    **What kind of source did you end up with: an API that needs a key, an open
    API, a site you have to parse, binary documents served over plain HTTP, or a
    hybrid? And what did access cost you in keys, quotas, rate limits, and
    waiting?**

    Answer in ~4-5 sentences. Use numbers you observed rather than numbers the
    documentation promises. Include roughly how long a full rebuild of your cache
    would take, and say whether that figure is timed or extrapolated. Check
    `robots.txt` on every host you touched, not just the main one: they are per
    host and they often disagree.

    Some ideas and examples to get you started: "metadata comes from \_\_\_\_\_ but the
    documents come from \_\_\_\_\_, so it is really a hybrid" or "\_\_\_\_\_ of my first \_\_\_\_\_
    requests came back HTTP \_\_\_\_\_" or "`\_\_\_\_\_/robots.txt` sets Crawl-delay \_\_\_\_\_, but
    `\_\_\_\_\_` has none at all" or "a rebuild takes about \_\_\_\_\_, extrapolated from \_\_\_\_\_
    rather than timed"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_4 = PLACEHOLDER
    mo.md(answer_4)
    return (answer_4,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part II, Section 2: the unit of document

    Recall Lab 1, Part II: the same 851,000 words of Shakespeare could be one
    document per play (38), per scene (791), or per speech (31,906), and the
    choice changed what questions the corpus could answer. The same choice
    faces you here, whether or not your source has an obvious record type.
    """)
    return


@app.cell
def _(records):
    # TODO(student): build a small table of candidate units for YOUR source,
    # finest to coarsest grain, each with a count, mirroring the Shakespeare
    # play/scene/speech example above. For a GitHub repo, that might be
    # commit / file / repo; for SEC filings, sentence / risk-factor section /
    # filing; for the ACL Anthology, paper / venue-year / venue. List at
    # least three candidates even if you only end up using one.
    units = pd.DataFrame([
        {"candidate unit": "TODO: finest grain", "n": None, "granularity": "finest"},
        {"candidate unit": "TODO: your chosen unit", "n": len(records), "granularity": "medium"},
        {"candidate unit": "TODO: coarsest grain", "n": None, "granularity": "coarsest"},
    ])
    units
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 5: What counts as one document

    **What is one document in your source, and which other granularities did you
    consider and reject?**

    Answer in ~3-4 sentences. Name one finer and one coarser alternative and say
    what is wrong with each for your question. If no level above yours exists in
    your source, say so, and say what that limits your claims to. This is the
    play / scene / speech choice from Lab 1 Part II, which moved the topics more
    than any hyperparameter did.

    Some ideas and examples to get you started: "one document is one \_\_\_\_\_, median
    \_\_\_\_\_ per document" or "one row per \_\_\_\_\_ has the larger n, but a lone \_\_\_\_\_ is
    uninterpretable without \_\_\_\_\_" or "there is no unit above \_\_\_\_\_ here, so any claim
    is about \_\_\_\_\_ specifically"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_5 = PLACEHOLDER
    mo.md(answer_5)
    return (answer_5,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part II, Section 3: extraction and its failure modes

    Pull out a field you need, and **measure how often it works** on the
    whole sample, not just the first few records. A rate with no denominator
    is not a finding.
    """)
    return


@app.function
def success_rate(items, is_success):
    """(n_success, n_total, rate_pct) for any predicate over any
    sequence. Reuse whether "success" means "had a determinable
    license" or "had a parseable checklist." Always report n_total."""
    n_total = len(items)
    n_success = sum(1 for it in items if is_success(it))
    rate_pct = round(100 * n_success / n_total, 1) if n_total else float("nan")
    return n_success, n_total, rate_pct


@app.cell
def _(records):
    # TODO(student): extract the field(s) you actually need from `records`,
    # then measure success with success_rate() above, on ALL of `records`,
    # not a sample you eyeballed. Example:
    #
    #   n_success, n_total, rate_pct = success_rate(records, lambda r: ...)
    #   print(f"{n_success}/{n_total} ({rate_pct}%) extracted cleanly")
    #
    # Look closely at whatever fails: a regex that returns nothing, a field
    # that is None for some records, an HTML tag structure that only some
    # pages use. Name each distinct failure mode you find; a vague "some
    # records were messy" is not a failure mode, "9/30 had no end marker"
    # (an SEC-row example) is one. Keep what you parsed out
    # (e.g. `extracted = [...]`) for Section 4.
    extracted = []
    print(f"extracted {len(extracted)} items from {len(records)} records")
    return (extracted,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 6: What counting revealed

    **How much of what you tried to extract came out usable, what went wrong with
    the rest, and what is actually in the part that worked?**

    Answer in ~5-6 sentences. Give every rate with its denominator, one per
    pipeline stage: "N of M documents had the section" and "N of M of those parsed
    cleanly" are different numbers and you need both. Describe the shape of what
    survived, and say whether what is missing is missing at random, pointing at
    numbers the way Part I did with coverage by medal sport. Say which of your
    failure modes you would have missed in a sample of five. If you found a bug in
    your own pipeline while doing this, describe it here instead of quietly fixing
    it: how you caught it is much more important for this assignment!

    Some ideas and examples to get you started: "\_\_\_\_\_ of \_\_\_\_\_ (X%) at the document
    level, and of those \_\_\_\_\_ of \_\_\_\_\_ at the \_\_\_\_\_ level" or "\_\_\_\_\_ failures were a \_\_\_\_\_
    artifact, where \_\_\_\_\_ split across a line break" or "coverage is great for this type of document
    but meh for this other type of document, so the missing ones are not a random sample" or "my first version
    paired \_\_\_\_\_ with \_\_\_\_\_ by position, which broke whenever \_\_\_\_\_"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_6 = PLACEHOLDER
    mo.md(answer_6)
    return (answer_6,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part II, Section 4: first look

    Basic EDA on `extracted`: counts, length distributions, and coverage
    across whatever strata matter for your source (time, venue, category,
    and so on).
    """)
    return


@app.cell
def _(extracted):
    # TODO(student): basic EDA on `extracted`. Report at least: total n, one
    # length statistic (e.g. median words, with its p10/p90 for spread) WITH
    # its denominator, and coverage across one stratum that matters for your
    # source (time period, venue, category, license, whatever your source
    # actually varies along). A plot is welcome but not required; printed
    # numbers with denominators satisfy this section on their own.
    print(f"n = {len(extracted)}")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part II, Section 5: one pre-registered question

    Write the hypothesis down BEFORE looking at the analysis below it.
    Otherwise it is too easy to convince yourself afterward that you always
    expected whatever you found.
    """)
    return


@app.cell
def _():
    # TODO(student): write YOUR hypothesis here, BEFORE running the analysis
    # cell below. State your prediction and why, in one or two sentences, in
    # a form that could turn out to be wrong: a direction (higher/lower), a
    # rough threshold, or a comparison between two groups in your data. Do
    # not edit this cell again after seeing the analysis output.
    rq_hypothesis_p2 = """
    Pre-registered, written before running the analysis in the next cell.

    TODO(student): your hypothesis here.
    """
    mo.md(f"**Pre-registered hypothesis:**\n{rq_hypothesis_p2}")
    return


@app.cell
def _(extracted):
    # TODO(student): run the analysis that tests your hypothesis above,
    # using `extracted` (or `records`). Print the actual numbers you get,
    # not just words -- a correlation, a group difference, a rate. Whatever
    # the result, it goes in Question 5 as-is: a null result that kills your
    # hypothesis is a legitimate result, not a reason to quietly change the
    # hypothesis after the fact.
    print(f"n = {len(extracted)}")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 7: Hypothesis, result, verdict

    You wrote `rq_hypothesis_p2` above before running the analysis, so this is a
    real pre-registration: you had a prior about your own source that you did not
    have about Wikipedia's headings in Part I.

    **What did you predict, what did the data say, and given that, can this source
    carry your group's project?**

    Answer in ~5-6 sentences. Report the result whether or not it supports you: a
    hypothesis that fails is a finding, and rewriting one after the fact is how a
    group fools itself. Then name the question this source is viable *for*, and a
    nearby question it cannot answer. Close with the caveat that matters most and
    where it has to be written down so a reader cannot miss it. Answering "no" is
    a good outcome for a proof of concept, and far cheaper now than in November.

    Some ideas and examples to get you started: "H1, registered above: \_\_\_\_\_" or "no
    support: \_\_\_\_\_ = \_\_\_\_\_, and splitting at the median gives \_\_\_\_\_ on both halves" or
    "viable for studying \_\_\_\_\_, not on its own for studying \_\_\_\_\_" or "a \_\_\_\_\_ means the
    authors claimed \_\_\_\_\_, not that \_\_\_\_\_ is actually true"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_7 = PLACEHOLDER
    mo.md(answer_7)
    return (answer_7,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---
    ## Part II, Section 6: blocker log, data card, and verdict

    Every blocker ends in `fixed` (you found a working path around it) or
    `deferred` (you chose not to solve it now, with an honest effort estimate
    and what it would unblock). Deferring is a legitimate, graded choice, not
    a failure: silently working around a problem without logging it is what
    actually loses credit.
    """)
    return


@app.cell
def _():
    # TODO(student): add at least one more row from YOUR OWN source below the
    # worked example. Every row ends in "fixed" or "deferred"; a deferred row
    # needs an honest effort estimate and what it would unblock.
    blocker_log = [
        {
            "what_broke": "S2's regular search endpoint 429'd on 6/6 rapid "
                "unauthenticated requests.",
            "how_i_noticed": "Printed HTTP status per call instead of "
                "trusting a silent retry.",
            "diagnosis": "The interactive search endpoint has a far tighter "
                "unauthenticated limit than the bulk endpoint.",
            "status": "fixed",
            "fix_or_estimate": "Switched to /paper/search/bulk: same query, "
                "unauthenticated, paginated not rate-limited.",
            "what_it_unblocks": "The full 4,544-record metadata pull every "
                "later section depends on.",
        },
        {
            "what_broke": "TODO",
            "how_i_noticed": "TODO",
            "diagnosis": "TODO",
            "status": "TODO: fixed or deferred",
            "fix_or_estimate": "TODO",
            "what_it_unblocks": "TODO",
        },
    ]
    pd.DataFrame(blocker_log)[["what_broke", "status", "what_it_unblocks"]]
    return


@app.cell
def _(extracted, records):
    # TODO(student): fill in the TODO fields below. "unknown, because ..." is
    # an acceptable value; a blank is not. n_documents/coverage should be
    # computed from `records`/`extracted` rather than typed, so the card
    # cannot drift out of date.
    data_card_p2 = {
        "name": "TODO",
        "source": "TODO",
        "snapshot_date": "TODO",
        "licence": "TODO",
        "document_unit": "TODO",
        "n_documents": len(extracted),
        "coverage": f"{len(extracted)}/{len(records)} records extracted cleanly",
        "known_biases": "TODO",
        "do_not_use_for": "TODO",
    }
    mo.md(
        "**Data card**\n\n"
        + "\n".join(f"- **{_k}**: {_v}" for _k, _v in data_card_p2.items())
    )
    return


if __name__ == "__main__":
    app.run()
