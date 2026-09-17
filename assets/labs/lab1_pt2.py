import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo

    import random
    import re
    import zipfile
    import urllib.request
    import xml.etree.ElementTree as ET
    from collections import Counter
    from pathlib import Path
    from datasets import load_dataset
    from matplotlib import pyplot as plt
    from sklearn.feature_extraction.text import CountVectorizer
    from tomotopy.models import LDAModel
    from tomotopy.utils import Corpus
    from tomotopy.coherence import Coherence
    import pandas as pd


@app.cell
def _():
    # --- Fill in your info ---------------------------------------------------
    NAME = ""
    ANDREW_ID = ""
    ASSIGNMENT = "Assignment 1, Part II"  # assignment name, or a one-line purpose
    DATE = ""  # e.g. 2026-09-01

    _missing = [
        _k
        for _k, _v in [
            ("NAME", NAME),
            ("ANDREW_ID", ANDREW_ID),
            ("ASSIGNMENT", ASSIGNMENT),
            ("DATE", DATE),
        ]
        if not _v.strip()
    ]
    _header = mo.md(
        f"# {ASSIGNMENT or '(untitled)'}\n\n"
        f"**Name:** {NAME or '(name)'}\n\n"
        f"**Andrew ID:** {ANDREW_ID or 'andrewID'}\n\n"
        f"**Date:** {DATE or '(date)'}"
    )
    _out = _header
    if _missing:
        _out = mo.vstack([
            _header,
            mo.callout(mo.md(f"Header incomplete. Fill in: {', '.join(_missing)}"), kind="warn"),
        ])
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Objectives

    In Part I of Lab 1, you worked with a clean corpus of newsgroup posts pre-sorted into 20 topics. You have developed some intuitions about how LDA topic model hyperparameters and other settings affect the kinds of topics that are generated. In Part II, you will experiment less thoroughly along the other axes (e.g. vocabulary thresholds, `alpha`, `eta,` seed-to-seed variation, etc.) and instead work with a slightly more open-ended corpus and engage with what that entails. The folks at Folger have invested significant resources to compiling clean, human- and machine-readable collections of William Shakespeare's works, so it might be a stretch to say that the corpus was found or collected "in the wild." That being said, you will still need to extract text to perform analyses for this assignment. You will:

    * Download and parse a real corpus from its source files: the Folger Shakespeare plays, distributed as TEI XML
    * Define what constitutes a "document" in three different ways and observe the effects on your topics
    * Observe the effects that preprocessing decisions have on the topics, as well as the corpus statistics
    * Compare what a topic model finds in Shakespeare with what it found in 20 Newsgroups
    * Form a hypothesis about Shakespeare's characters and use a topic model to test it

    ## Allowed and recommended resources
    * assistance from course staff
    * provided scaffolding in starter notebook
    * official documentation such as through `help(LDAModel)` and the official page, or `man unzip` in your terminal
    * piazza Q&A (your own questions and/or others’)
    * other course materials (e.g. released in-class activities)
    * internet for general resources to understand subject material
    * speech-to-text software to help transcribe answers


    **When you are finished, submit this marimo notebook, filled out with your answers, along with the auto-saved `model_history_part2.csv` record of the models you trained (more below).**

    Questions are numbered h2 headings (`## Question N`) with an `answer_N` cell right below, and the registry at the top collects your answers.
    """)
    return


@app.cell
def _():
    # [CLAUDE-DRAFT]
    QUESTIONS = {
        1: "Three ways to make a document",
        2: "Shakespeare vs. 20 Newsgroups",
        3: "Form and test a hypothesis",
    }
    PLACEHOLDER = "(write your answer here)"
    return PLACEHOLDER, QUESTIONS


@app.cell
def _(answer_1, answer_2, answer_3):
    ANSWERS = {1: answer_1, 2: answer_2, 3: answer_3}
    # answer variables are defined throughout the notebook. Marimo does not track in place dictionary writes, so we need to explicitly define the dictionary here.
    return (ANSWERS,)


@app.cell(hide_code=True)
def _(ANSWERS, PLACEHOLDER, QUESTIONS):
    _rows, _done = [], 0
    for _n, _title in QUESTIONS.items():
        _a = ANSWERS.get(_n, "").strip()
        _ok = bool(_a) and _a != PLACEHOLDER.strip()
        _done += _ok
        _rows.append(
            f"**{'✅' if _ok else '⬜'} Question {_n}: {_title}**\n\n"
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


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Getting the data

    The [Folger Shakespeare Library](https://www.folger.edu) publishes each play (and a collection of his complete works) as a zip of TEI XML (plus HTML and PDF and plain-text versions). You will download the XML data, parse it, and use its structure to help you form your analysis. We use the XML forms because it contains tags for structure we want: acts, scenes, speeches, and character names. The HTML has the same text but no clean per-speech wrapper, and the plain text has no labeled structure at all.

    **Disclaimer: This should work on most Macs. If some of this does not work for you e.g. because you are on a Windows machine or use a slightly different command-line interface, feel free to look beyond this notebook for resources**

    In your preferred command-line interface (e.g. Terminal if you are on a MacBook) (**outside of this marimo notebook**):

    1. **Download** the complete-works XML zip (about 22 MB). On the Folger [download page](https://www.folger.edu/explore/shakespeares-works/download/), under "Shakespeare's Works", choose the **XML** option for the complete works. Or fetch it directly:

    ```bash
    cd path/to/your/11811/code/dir
    curl -L -O https://shakespeare.folger.edu/downloads/xml/shakespeares-works_XML_FolgerShakespeare.zip
    ```

    (`-L` follows the redirects; the file is served from an [S3](https://aws.amazon.com/s3/) bucket)

    2. **Extract** the outer and inner zips. The outer zip holds 42 inner zips, one per play/poem. Each inner zip holds one `.xml` file plus images and a stylesheet we will ignore for this assignment.

    ```bash
    unzip shakespeares-works_XML_FolgerShakespeare.zip
    cd shakespeares-works_XML_FolgerShakespeare
    for each in *.zip;
    do
    unzip -q $each;
    mv ${each%%.*} ${each%_*};
    done
    ```
    That last `mv` line from the for loop just renames directory names to be slightly shorter. Technically optional.

    (If you see any `__MACOSX` directories appear as you unzip things, feel free to delete them! e.g. `rm -r __MACOSX` or `rm -r */__MACOSX`)

    Note: You can also do this in Python with `zipfile` and `pathlib` instead

    **3. Check the layout.** You should end up with 42 files shaped like `<play>_XML/<CODE>.xml`, for example `hamlet_XML/Ham.xml`. Both of these lines below should show you 42

    ```bash
    ls *.zip | wc -l
    ls -p | grep XML/ | wc -l
    ```

    Four of the 42 are poems (`Son.xml` the sonnets, `Luc.xml` *Lucrece*, `Ven.xml` *Venus and Adonis*, `PhT.xml` *The Phoenix and Turtle*). We will ignore these for this assignment and work with only the 38 plays.
    """)
    return


@app.cell
def _():
    XML_OUTER_DIR = "shakespeares-works_XML_FolgerShakespeare"
    XML_DIR = (mo.notebook_dir() or Path.cwd()) / XML_OUTER_DIR

    POEMS = ["Luc", "Son", "PhT", "Ven"] # excluded

    xml_paths = sorted(p for p in XML_DIR.glob("*/*.xml") if "__MACOSX" not in p.parts)
    if xml_paths:
        _msg = mo.md(f"Found **{len(xml_paths)}** XML files under `{XML_DIR}`; {len([p for p in xml_paths if p.stem in POEMS])} poems will be skipped.")
    else:
        _msg = mo.callout(mo.md(f"No XML files found under `{XML_DIR}`. Follow the three steps above, then re-run this cell."), kind="danger")
    _msg
    return POEMS, xml_paths


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Parsing TEI XML

    Before reading on, open one of the `.xml` files in a text editor (e.g. `shakespeares-works_XML_FolgerShakespeare/hamlet_XML/Ham.xml`) and take a look around. It looks nothing like the strings we got from 20 Newsgroups. Every single word is its own element:

    ```xml
    <sp xml:id="sp-0001" who="#Countess_AWW">
      <speaker xml:id="spk-0001"><w xml:id="w0000440">COUNTESS</w></speaker>
      <ab xml:id="ab-0001">
        <w xml:id="w0000450" n="1.1.1">In</w>
        <c xml:id="c0000460" n="1.1.1"> </c>
        <w xml:id="w0000470" n="1.1.1">delivering</w>
        ...
        <w xml:id="w0000550" n="1.1.1">me</w>
        <pc xml:id="p0000560" n="1.1.1">,</pc>
        ...
        <w xml:id="w0000640" n="1.1.1">second</w>
        <lb xml:id="lb-00010"/>
        <w xml:id="w0000650" n="1.1.2">husband</w>
        <pc xml:id="p0000660" n="1.1.2">.</pc>
      </ab>
    </sp>
    ```

    `xml` files are often more easily parse-able than these, in that each textual element might contain a full sentence or paragraph, but in any case the structure offered here is useful to us.

    Here `<w>` is a word, `<c>` is a space, `<pc>` is a punctuation mark, and `<lb/>` is a line break (note that there is no space before the next word). A `<sp>` is one speech, and its `who` attribute is Folger's id for the character speaking. Acts are `<div1 type="act">` elements, scenes are `<div2 type="scene">` elements nested inside them, and prologues, epilogues, choruses and inductions get their own `div`s with their own `type`.

    There is also a fair amount of text in here that looks like dialogue but isn't: `<speaker>` labels, `<stage>` directions (these are tokenized into `<w>` elements too, so we have to skip the whole subtree rather than just the tag), `<fw>` running page headers like "ACT 1. SC. 1", and `<app>` blocks that hold an alternative reading of a word that is already in the text. The parser below skips all of these. We encourage you to read through it-- it is only about 40 lines, and the decisions it makes (what counts as a speech, which text to keep, where to put whitespace) are preprocessing decisions just as much as lowercasing or stopword removal are

    We use the Python standard library's `xml.etree.ElementTree`. TEI files use an XML namespace, which is why every tag in the code below is prefixed with `{http://www.tei-c.org/ns/1.0}`.
    """)
    return


@app.cell
def _():
    # TEI parser. Returns one dict per speech.
    def tag(el):                                   # "{http://www.tei-c.org/ns/1.0}w" -> "w"
        return el.tag.split("}")[-1]

    TOKENS = {"w", "c", "pc"}                               # word, space, punctuation mark
    NOT_DIALOGUE = {"speaker", "stage", "sound", "app"}     # their tokens are not spoken lines

    def text_of(element, skip=NOT_DIALOGUE):
        """The spoken text under `element`: its word/space/punctuation tokens in document order, a newline
        at every <lb/>, leaving out everything inside a speaker label, stage direction, sound cue or <app> note."""
        hidden = {el for bad in element.iter() if tag(bad) in skip for el in bad.iter()}
        parts = []
        for el in element.iter():
            if tag(el) == "lb":
                parts.append("\n")
            elif tag(el) in TOKENS and el not in hidden:
                parts.append("".join(el.itertext()))
        lines = "".join(parts).split("\n")
        return "\n".join(line.rstrip() for line in lines).strip()

    def parse_play(path):
        """One Folger TEI file -> a list of speech dicts: play, title, act, scene, scene_type, who, speaker, text."""
        root = ET.parse(path).getroot()
        code = Path(path).stem
        title = root.findtext(".//{*}titleStmt/{*}title", default=code).strip() or code
        body = root.find(".//{*}text/{*}body")

        # 1. the scene units: numbered scenes get an "act.scene" label; prologues, choruses, etc. keep their own
        units = []                                                        # (element, act, label, kind)
        for div1 in body.findall("{*}div1"):
            if div1.get("type") == "act":
                act = div1.get("n")
                for div2 in div1.findall("{*}div2"):
                    n = div2.get("n")
                    if n.isdigit():
                        units.append((div2, act, f"{act}.{n}", "scene"))
                    else:
                        units.append((div2, act, n, div2.get("type")))           # "2.CHO", "EPI"
            else:
                units.append((div1, None, div1.get("n"), div1.get("type")))      # top-level prologue / induction / epilogue

        # 2. one row per speech
        rows = []
        for unit, act, label, kind in units:
            for sp in unit.iterfind(".//{*}sp"):
                speaker = sp.find("{*}speaker")
                rows.append({
                    "play": code, "title": title, "act": act, "scene": label, "scene_type": kind,
                    "who": sp.get("who", "").replace("#", "") or "(unattributed)",
                    "speaker": "" if speaker is None else text_of(speaker, skip=()),
                    "text": text_of(sp),
                })
        return rows

    return (parse_play,)


@app.cell
def _(POEMS, parse_play, xml_paths):
    # parse every play into one DataFrame of speeches
    mo.stop(not xml_paths, mo.md("_No XML files found. Fix the download cell above first._"))
    speeches = pd.DataFrame([_row for _p in xml_paths if _p.stem not in POEMS for _row in parse_play(_p)])
    speeches
    return (speeches,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Before we build anything on top of the parse, let's confirm: You should see **38 plays, 31,906 speeches, and 791 scenes** (770 numbered scenes, plus 21 prologues, epilogues, choruses and inductions that we treat as scenes). Two of the speeches are empty: one is a `<gap/>` where the source text has been lost, and the other is Marina's "sings" in *Pericles, Prince of Tyre* with no words given. 157 speeches have more than one id in `who`, i.e. lines spoken by several characters at once. If your numbers are different, something probably went wrong in the download or extraction step, so take a look there first!

    The last output is one speech, reassembled from its `<w>`, `<c>` and `<pc>` elements. Compare it against the XML snippet above: the `<lb/>` turned into a newline and the `<c>` spaces survived, so the text reads as verse. Also note the apostrophe in "man's"-- it is the curly U+2019 character rather than the ASCII `'`. Keep this in mind; it will come back in Question 2.
    """)
    return


@app.cell
def _(speeches):
    _units = speeches.drop_duplicates(["play", "scene"])
    mo.vstack([
        mo.md(f"**Plays:** {speeches['play'].nunique()}"),
        mo.md(f"**Speeches:** {len(speeches)}"),
        mo.md(f"**Scenes:** {len(_units):}"),
        mo.md(f"({(_units['scene_type'] == 'scene').sum()} numbered scenes; other unit types: {_units.loc[_units['scene_type'] != 'scene', 'scene_type'].value_counts().to_dict()}). "),
        mo.md(f"Empty speeches: {(speeches['text'] == '').sum()}. Shared-line speeches: {speeches['who'].str.contains(' ').sum()}."
        ),
        mo.md(f"First speech of `{speeches.loc[0, 'play']}` {speeches.loc[0, 'scene']}, `{speeches.loc[0, 'who']}`:\n\n```\n{speeches.loc[0, 'text']}\n```"),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Varying document definitions

    In Part I the corpus had already been set up to define each newgroup post as a document. Here, we must make a conscious choice on where and how to draw boundaries btween documents: The same 851k words can be one document per **play** (38 long documents), one per **scene** (791 medium documents), or one per **speech** (31,906 short ones). Since LDA is a model of documents, this can be an especially consequential decision

    `build_docs` groups the speech table by any set of columns and joins the text together. We build the corpus structure in three ways below. The same function also gives you two character-based splits, in case you want them for Question 3 or are just curious: all of one character's lines within a play, and all of one character's lines across the whole corpus. (Note: Folger reuses a character id across plays for recurring historical figures, e.g. `Antony_JC` appears in both *Julius Caesar* and *Antony and Cleopatra*, so the whole-corpus split merges those. It does not merge unrelated characters who happen to share a name-- there are five different Antonios!)

    Each document definition is a pair `(texts, meta)`: a list of document strings, and a DataFrame with one row per document telling you where it came from. Keep them together; you'll want `meta` when you try to interpret topics.
    """)
    return


@app.cell
def _(speeches):
    def build_docs(table, by):
        """Group `table` (the speeches DataFrame) by the column(s) in `by` and join the text with newlines.
        by=None keeps every speech as its own document. Returns (texts: list[str], meta: DataFrame)."""
        if by is None:
            meta = table[["play", "act", "scene", "scene_type", "who", "speaker"]].reset_index(drop=True)
            texts = table["text"].tolist()
        else:
            by = [by] if isinstance(by, str) else list(by)
            g = table.groupby(by, sort=False)
            meta = g.agg(n_speeches=("text", "size"), speakers=("who", lambda s: ", ".join(sorted(set(s))))).reset_index()
            texts = g["text"].apply("\n".join).tolist()
        meta.insert(0, "doc_id", range(len(texts)))   # index into `texts`; survives the empty-doc filtering later
        return texts, meta

    DOC_CFG = {
        "play":   build_docs(speeches, "play"),
        "scene":  build_docs(speeches, ["play", "scene"]),
        "speech": build_docs(speeches, None),
    }
    # character splits (used in a later question)
    character_per_play = build_docs(speeches, ["play", "who"])
    character_corpus = build_docs(speeches, "who")
    # character documents have a long tail of one-line parts, so the form also offers a filtered version
    CHARACTER_MIN_TOKENS = 50   # whitespace-separated words; change it here if you want a different cutoff
    _keep = [_i for _i, _t in enumerate(character_per_play[0]) if len(_t.split()) >= CHARACTER_MIN_TOKENS]
    _meta_long = character_per_play[1].iloc[_keep].reset_index(drop=True)
    _meta_long["doc_id"] = range(len(_keep))   # re-number so doc_id indexes the filtered text list
    character_per_play_long = ([character_per_play[0][_i] for _i in _keep], _meta_long)
    ALL_DOCS = {   # everything the form below can train on
        **DOC_CFG,
        "character_per_play": character_per_play,
        f"character_per_play (>={CHARACTER_MIN_TOKENS} tokens)": character_per_play_long,
        "character_corpus": character_corpus,
    }

    mo.md(
        "Documents per configuration: " + ", ".join(f"**{_k}** = {len(_v[0]):,}" for _k, _v in DOC_CFG.items())
        + f"; character-per-play = {len(character_per_play[0]):,} ({len(character_per_play_long[0]):,} with at least {CHARACTER_MIN_TOKENS} tokens); character (whole corpus) = {len(character_corpus[0]):,}."
    )
    return ALL_DOCS, DOC_CFG


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Taking a closer look at the corpus

    Some notation first. The corpus is a list of documents $d_1, \dots, d_D$. Run the analyzer over every document and you get a list of **tokens**, i.e. word occurrences. Linguists call each distinct token a **type**, so "the cat sat on the mat" has 6 tokens and 5 types (`the` occurs twice). Let $N$ be the total number of tokens in the corpus and $V$ the number of types (the vocabulary size). We can write $\mathrm{count}(w)$ for how many times type $w$ occurs in the whole corpus, and $n_d$ / $v_d$ for the number of tokens / types inside document $d$ specifically.

    Terms mapped to table columns:

    * `n_docs` $= D$, the number of documents. `n_tokens` $= N$. `n_types` $= V$, the number of distinct tokens.
    * `type_token_ratio` $= V / N$, over the whole corpus. Usually shortened to **TTR**. A corpus that keeps reusing the same words has a low TTR; a corpus that keeps introducing new words has a high one.
    * `hapax_types` $= |\{w : \mathrm{count}(w) = 1\}|$, the number of types that occur exactly once in the whole corpus. Linguists call these *hapax legomena*, Greek for "said once". `hapax_frac_of_types` $=$ `hapax_types` $/ V$, the share of the vocabulary that is one-offs: typos, rare names, one-time coinages.
    * `mean_types_doc` $= \frac{1}{D}\sum_d v_d$, the average number of distinct tokens per document. `mean_ttr_doc` $= \frac{1}{D}\sum_d v_d / n_d$, the average of each document's *own* TTR (empty documents are left out of this one).
    * `doc_len_mean`, `doc_len_median`, `doc_len_min`, `doc_len_max`: mean, median, min and max of $n_d$. `empty_docs`: how many documents have $n_d = 0$.
    * `top_tokens`: the ten types with the largest $\mathrm{count}(w)$.

    E.g. take two documents, $d_1=$`the cat sat here` and $d_2=$`the dog sat on the cat`. Then $N = 10$ and $V = 6$ (`the`, `cat`, `sat`, `here`, `dog`, `on`), so `type_token_ratio` $= 6/10 = 0.6$; the one-offs are `dog`, `here`, and `on`, so `hapax_types` $= 3$ and `hapax_frac_of_types` $= 3/6 = 0.5$. Inside the documents, $v_1 / n_1 = 4/4 = 1.0$ and $v_2 / n_2 = 5/6 \approx 0.83$, so `mean_types_doc` $= 4.5$ and `mean_ttr_doc` $\approx 0.92$.

    Now, if we combine the two documents into one: $N$, $V$, the TTR and the hapax numbers are corpus aggregates and do not change, but `mean_types_doc` becomes $6$ and `mean_ttr_doc` becomes $6/10 = 0.6$.

    One thing to keep in mind: corpus-wide TTR goes down as a corpus gets bigger. Common words keep repeating while new words run out, so $V$ grows much more slowly than $N$. That means you can't directly compare the raw TTR of an ~850k-token corpus with that of a ~2.4M-token one. `ttr_at_500k_sample` accounts for this by drawing a random sample of exactly 500,000 tokens (with a fixed seed) and computing $V/N$ on the sample, which *is* comparable across corpora. (It will give you a `NaN` for a corpus smaller than 500k tokens)
    """)
    return


@app.cell
def _():
    # copied from pt 1
    vectorizer = CountVectorizer(
        strip_accents="unicode", # whether to strip unicode characters of their accents, and to make them into their ascii "equivalents", e.g. é -> e
        lowercase=False, # whether to lowercase everything
        stop_words=None, # whether to remove stopwords
        token_pattern=r"(?u)\b\w+\b",
        ngram_range=(1,1), # the range of n-grams to consider. (1,2), e.g. would consider unigrams and bigrams.
        analyzer="word",
        max_df=1.0,
        min_df=1,
    )
    analyzer = vectorizer.build_analyzer()
    return analyzer, vectorizer


@app.cell
def _():
    def corpus_stats(texts, analyzer, top_n=10, ttr_sample_n=500_000):
        """texts: list of document strings. analyzer: a CountVectorizer analyzer (text -> list of tokens).
        Returns a dict of corpus statistics; see the definitions above."""
        token_lists = [analyzer(t) for t in texts]
        counts = Counter(t for toks in token_lists for t in toks)
        lens = pd.Series([len(t) for t in token_lists])
        n_tok, n_types = int(lens.sum()), len(counts)
        hapax = sum(1 for c in counts.values() if c == 1)
        doc_types = pd.Series([len(set(t)) for t in token_lists])
        doc_ttr = pd.Series([len(set(t)) / len(t) for t in token_lists if t])
        ttr_sample = float("nan")
        if n_tok >= ttr_sample_n:
            flat = [t for toks in token_lists for t in toks]
            ttr_sample = len(set(random.Random(0).sample(flat, ttr_sample_n))) / ttr_sample_n
        return {
            "n_docs": len(texts),
            "n_tokens": n_tok,
            "n_types": n_types,
            "type_token_ratio": n_types / n_tok if n_tok else float("nan"),
            "ttr_at_500k_sample": ttr_sample,
            "hapax_types": hapax,
            "hapax_frac_of_types": hapax / n_types if n_types else float("nan"),
            "mean_types_doc": float(doc_types.mean()),
            "mean_ttr_doc": float(doc_ttr.mean()),
            "doc_len_mean": float(lens.mean()),
            "doc_len_median": float(lens.median()),
            "doc_len_min": int(lens.min()),
            "doc_len_max": int(lens.max()),
            "empty_docs": int((lens == 0).sum()),
            "top_tokens": " ".join(t for t, _ in counts.most_common(top_n)),
        }

    def stats_table(named_text_lists, analyzer):
        """{name: texts} -> one row per name, rounded for display."""
        df = pd.DataFrame({n: corpus_stats(t, analyzer) for n, t in named_text_lists.items()}).T
        for c in ("type_token_ratio", "ttr_at_500k_sample", "hapax_frac_of_types", "mean_ttr_doc"):
            df[c] = df[c].astype(float).round(4)
        for c in ("mean_types_doc", "doc_len_mean"):
            df[c] = df[c].astype(float).round(1)
        return df

    return (stats_table,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    We also load 20 Newsgroups again here, so that the same statistics can sit side by side in one table. Take a look at the table before moving on to Question 1: which columns are identical across play / scene / speech, and which are not? Think about why that is. The identical columns are properties of the **text** itself; the others are properties of how we chose to **split** it.
    """)
    return


@app.cell
def _():
    # Part I corpus, for comparison rows
    newsgroups_train = load_dataset("SetFit/20_newsgroups", split="train")
    newsgroups_texts = list(newsgroups_train["text"])
    return newsgroups_texts, newsgroups_train


@app.cell
def _(DOC_CFG, analyzer, newsgroups_texts, stats_table):
    # statistics for three configs of "doc" + 20NG, using the Part I analyzer
    base_stats = stats_table({**{_k: _v[0] for _k, _v in DOC_CFG.items()}, "20newsgroups (post)": newsgroups_texts}, analyzer)
    mo.vstack([
        mo.ui.table(base_stats.drop(columns=["top_tokens"]).reset_index().rename(columns={"index": "documents"}), selection=None, pagination=False),
        mo.md("Top 10 tokens: " + "; ".join(f"**{_k}**: {_v}" for _k, _v in base_stats["top_tokens"].items())),
    ])
    return (base_stats,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Topic modeling again

    Every model in this section starts from one configuration, `BASELINE_PT1Q2`, so that whatever differs between two models is due to something you changed on purpose: the document definition, the preprocessing, or (once you get to the form further down) the hyperparameters themselves.

    For now, we have filled out the `basic_topic_model` settings (k=20, alpha=0.1, eta=0.01, seed=42, 1000 training steps, no vocabulary pruning) from Part I for `BASELINE_PT1Q2`. **Please replace these settings with the values you settled on in Part I Question 2 instead\*, and report them in your text answer below!** (The name is a reminder that these are *your* Part I Question 2 values, not tomotopy's defaults.)

    \*One note about `min_df`: it counts *documents*, so the same `min_df=20` means "appears in more than half of the plays" with play documents but "appears in a tiny fraction of speeches" with speech documents. Feel free to swap between `min_df` and `min_cf` (which counts tokens across the corpus) if you want a frequency threshold that means the exact same thing across Shakespeare document definitions, or feel free leave `min_df` as is and just be aware of the difference + report it in your answer either way.

    The helpers below are copied over from Part I. `show_topics` prints one row per topic with its share of tokens, how many of its top words are on scikit-learn's English stopword list, and the top words themselves. `train_lda` builds, fills, and trains a model and returns it along with its log-likelihood trace. Its default corpus is `tokenized_docs`, i.e. the scene documents. Pass `docs=` for anything else.
    """)
    return


@app.cell
def _():
    # TODO: copy your Part I Question 2 settings here. The values here are the Part I basic_topic_model placeholders: replace them! 
    # AND report the settings in your Part II Question 1 answer below (can literally be a copy paste of the line below)
    BASELINE_PT1Q2 = dict(k=20, alpha=0.1, eta=0.01, seed=42, iters=1000, min_cf=0, min_df=0, rm_top=0)
    return (BASELINE_PT1Q2,)


@app.cell
def _():
    # copied from pt 1
    # compact topic table, reused for every model from here on
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as _STOP_WORDS  # 318 lowercase words

    def show_topics(model, top_n=10):
        """One row per topic: topic id, share of the model's kept tokens assigned to it,
        number of its top words that are English stop words (case-insensitive), top words."""
        counts = model.get_count_by_topics()
        total = sum(counts)
        rows = [f"| topic | % of kept tokens | stop words in top {top_n} | top words |", "|---|---|---|---|"]
        for k in range(model.k):
            top = [w for w, _p in model.get_topic_words(k, top_n=top_n)]
            n_stop = sum(w.lower() in _STOP_WORDS for w in top)
            rows.append(f"| {k} | {100 * counts[k] / total:.1f} | {n_stop} | {', '.join(top)} |")
        return mo.md("\n".join(rows))

    return (show_topics,)


@app.cell
def _(DOC_CFG, analyzer):
    # tokenize each setting once with the Part I analyzer; drop empty docs and keep meta aligned
    def tokenize_cfg(texts, meta, analyzer):
        """Returns (token_lists, meta) with empty documents removed from both, so row j of meta describes token list j."""
        toks = [analyzer(t) for t in texts]
        keep = [i for i, t in enumerate(toks) if t]
        return [toks[i] for i in keep], meta.iloc[keep].reset_index(drop=True)

    TOKENIZED = {_k: tokenize_cfg(_v[0], _v[1], analyzer) for _k, _v in DOC_CFG.items()}
    tokenized_docs, scene_meta = TOKENIZED["scene"] # default is scene for parts of the assignment
    mo.md("Non-empty documents after tokenizing: " + ", ".join(f"**{_k}** = {len(_v[0]):,}" for _k, _v in TOKENIZED.items()))
    return TOKENIZED, tokenize_cfg, tokenized_docs


@app.cell
def _(tokenized_docs):
    # copied verbatim from pt 1
    # NOTE: fix_alpha=False (tomotopy's optim_interval=10) is the default, so by default alpha will tend to converge
    # throughout training. fix_alpha=True keeps it at the value you pass. Other than on Question 5, we leave
    # the default. Question 5 asks students to tick the "Fix alpha" box
    def train_lda(k=20, alpha=0.1, eta=0.01, seed=42, iters=1000, min_cf=0, min_df=0, rm_top=0,
                  docs=None, log_every=100, fix_alpha=False, workers=0):
        """Build an LDAModel with these settings, add every document in `docs` (default: tokenized_docs),
        and train for `iters` Gibbs sampling steps.

        fix_alpha: tomotopy re-estimates alpha every 10 steps by default (optim_interval=10), so the alpha
        you pass is only a starting value that tends to converge to a common valuethroughout training.
        Setting fix_alpha=True sets optim_interval=0, and alpha stays at the value you pass in at invocation.
        Question 5 asks for True since it is explicitly about varying alpha and eta. Everywhere else leaves
        the default, which matches basic_topic_model.
        workers: threads for training; 0 means all cores. tomotopy warns that same-seed runs can differ when
        workers != 1. We could theoretically pass workers=1 for a strict same-seed comparison, which is slower.
        BUT in practice we didn't notice any real variation from run to run as long as random seed was the
        same, so we leave the default of 0 for speed.

        Returns (model, trace). `trace` is a list of (step, log-likelihood per word, perplexity), one entry
        every `log_every` steps, so you can plot how training went."""
        model = LDAModel(k=k, alpha=alpha, eta=eta, seed=seed, min_cf=min_cf, min_df=min_df, rm_top=rm_top)
        model.optim_interval = 0 if fix_alpha else 10
        for doc in (tokenized_docs if docs is None else docs):
            model.add_doc(doc)
        trace = []
        done = 0
        while done < iters:
            step = min(log_every, iters - done)
            model.train(step, workers=workers)
            done += step
            trace.append((model.global_step, model.ll_per_word, model.perplexity))
        return model, trace

    return (train_lda,)


@app.cell
def _(BASELINE_PT1Q2, log_run, train_lda):
    # train with BASELINE_PT1Q2 settings (plus any overrides), append a row to model_history_part2.csv, return the model
    def run_model(label, docs, **overrides):
        """label: short name, printed with the result and written to the CSV (e.g. "scene / part1-vectorizer").
        docs: list of token lists. overrides: any settings you want to change from the baseline; report them in your answer."""
        settings = {**BASELINE_PT1Q2, **overrides}
        model, trace = train_lda(docs=docs, **settings)
        log_run(label, "run_model", label, settings, model, trace)
        print(f"{label}: {len(model.docs):,} docs, kept {len(model.used_vocabs):,} of {len(model.vocabs):,} distinct tokens, "
              f"log-likelihood/word {model.ll_per_word:.3f}")
        return model

    return (run_model,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Question 1: Three ways to make a document

    The cell below trains one model per document definition (play, scene, speech), with `BASELINE_PT1Q2` settings and the Part I tokenizer. Look at the three topic tables and at the statistics table above.

    **Answer in ~6-8 sentences:** a) What kind of thing do the topics capture under each document definition (subject matter? which play it is? who is talking, or how? something else)? b) Which statistics change across the doc definitions and which do not, and does that match what the topics did? c) If you wanted a topic model that found *themes* in Shakespeare (love, death, war, money), which document definition would you choose, and what would you still be worried about?

    Discuss what you believe "should" happen from theory, *and then* write down what you see in the three tables + explain it.

    You should address all three sub-questions, but when discussing expectations vs observations and post-hoc explanations, there is no need to fully address all components with the same depth (e.g. it is okay to focus on just one or two notable observations)

    Some ideas and examples to get you started: "with play documents every topic was basically a list of character names from one or two plays, because \_\_\_\_\_" or "with speech documents I got a topic for 'thou thy thee' and another for 'you your', which is not a topic about anything, it is \_\_\_\_\_" or "mean document TTR went from \_\_\_\_\_ to \_\_\_\_\_ but the corpus TTR did not move, because \_\_\_\_\_" or "the scene documents had one topic about fathers, sons and death that neither other definition had"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_1 = rf"""
    {PLACEHOLDER}
    """
    return (answer_1,)


@app.cell
def _(TOKENIZED, run_model, show_topics):
    # three models, one for each doc def
    shakespeare_models = {_docdef: run_model(f"{_docdef} / part1-vectorizer", _toks) for _docdef, (_toks, _meta) in TOKENIZED.items()}
    mo.ui.tabs({f"{_docdef} ({len(TOKENIZED[_docdef][0]):,} docs)": show_topics(_m, top_n=12) for _docdef, _m in shakespeare_models.items()})
    return (shakespeare_models,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Preprocessing again

    In Part I Question 7 you changed the `CountVectorizer` and looked at what happened to the topics. As part of the next question, you will do this again on Shakespeare scene documents.

    One potential issue in preprocessing this corpus: The Part I token pattern `\b\w+\b` matches runs of "word characters" (letters, digits, underscore) and cuts a token at anything else. An apostrophe is not a word character, so every contraction and possessive gets cut in two: "man's" becomes the tokens `man` and `s`, "I'll" becomes `I` and `ll`, "o'er" becomes `o` and `er`, "th'" becomes `th`, and "'tis" becomes `tis`. The fragments are frequent (in the 38 plays: `s` 7,499 times, `ll` 2,592, `t` 1,293, `th` 1,240, `st` 1,039, `tis` 692, `er` 646), they are not on scikit-learn's English stopword list, and they are not real words, so they can end up as top words of a topic. Scroll back up to the Question 1 topics and you may find `s`, `ll`, `th`, `er`, `st` sitting in the top words (depending on your specific model's settings). Check for these in the cell below

    This happens for both 20 Newsgroups and Shapkespeare, but the two corpora use different apostrophe tokens, so if you want "don't" to be its own word, you might need a different regex to make that happen in Shakespeare vs 20 Newsgroups.

    Shakespeare uses the curly U+2019 `’` everywhere, while 20 Newsgroups uses the straight ASCII `'` everywhere.

    Three reasonable solutions (pick one):

    * Keep the contraction whole: token pattern `r"(?u)\b\w+(?:'\w+)?\b"`. "don't" and "I'll" then become frequent whole tokens (that can be removed via `rm_top`, or kept).
    * Drop the clitics: scikit-learn's default `\b\w\w+\b` does this by dropping 1-character tokens ("man's" → `man`). It also drops "I" and "O" but keeps `ll`, `er`, `th`, `st`.
    * Don't do anything, filter after: a minimum token length (`r"(?u)\b[a-zA-Z]{3,}\b"`) or `min_cf`. Removes real short words too.

    Any of these must match the apostrophe actually in the text. The first pattern fixes 20 Newsgroups and does nothing on Shakespeare, since `’` is not `'`. Either convert `’` to `'` in `normalize` (the commented-out line does this) or accept both: `r"(?u)\b\w+(?:[’']\w+)?\b"`. Always check the actual characters before trusting a regex!
    """)
    return


@app.cell
def _(DOC_CFG, analyzer, newsgroups_texts):
    # how many apostrophe fragments does the Part I tokenizer create?
    _shakes = "\n".join(DOC_CFG["play"][0])
    _news = "\n".join(newsgroups_texts)
    _frag = ["s", "t", "ll", "d", "re", "ve", "er", "em", "tis", "th"]
    _c_s = Counter(t for t in analyzer(_shakes) if t in _frag)
    _c_n = Counter(t for t in analyzer(_news) if t in _frag)
    pd.DataFrame({
        "Shakespeare (U+2019 count = %d, ASCII ' = %d)" % (_shakes.count("’"), _shakes.count("'")): _c_s,
        "20 Newsgroups (U+2019 count = %d, ASCII ' = %d)" % (_news.count("’"), _news.count("'")): _c_n,
    }).fillna(0).astype(int).reindex(_frag)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Question 2: Shakespeare vs. 20 Newsgroups

    ### 2a. Tune a topic model

    Using the form below, train a Shakespeare topic model you find useful or informative. Feel free to either iterate from `BASELINE_PT1Q2` or start from scratch. You will have to choose a document definition, the preprocessing pipeline (`normalize` + `vectorizer_v2` in the cells below e.g. the apostrophe fix), and the LDA hyperparameters. Train at least 4 and at most about 10 runs, and keep them in `model_history`. **Report the settings of your final model (documents, preprocessing, every form field, seed) and either paste its topic table or describe its topics in ~2 sentences. Additionally, you will be turning in `model_history_shakespeare.csv` which will be auto-saved as you train your models.**

    Note: `normalize` runs on the raw text before the vectorizer sees it, and `vectorizer_v2` is the Part I vectorizer with every knob exposed. Each time you change either one, the statistics table right after them recomputes for all three document definitions next to the Part I baseline, and the form re-tokenizes its documents with your new preprocessing

    ### 2b. Compare between corpora

    Press the button further down to train the 20 Newsgroups reference model once (`BASELINE_PT1Q2`, Part I vectorizer), then pick it in the "Model to inspect" dropdown so you can read its documents next to your Shakespeare models. **In ~6 sentences, compare the two corpora on two fronts:**

    a) Outcomes: What does a "topic" turn out to be in each corpus? What is similar and what is different between corpora? Roughly how many of the 20 topics in each are a subject you could put a name to, and what are the rest (names, register, formatting, junk)? Back up at least one statement with something from the statistics table or other corresponding evidence.

    b) Process: How did you decide whether a topic was "good" in each corpus, and did you have to change how you looked? Did any hyperparameters or other settings feel more or less sensitive here than in Part I, and if so, what is your best guess about why (document length? vocabulary size? the corpus itself)? Did anything you "knew" from Part I turn out to be about 20 Newsgroups vs about topic models in general?

    Some ideas and examples to get you started: "I couldn't skim 800-token verse scenes the way I skimmed newgroup posts, so I ended up judging topics mostly by which characters were in them" or "alpha barely did anything on play documents but flipped speech documents from one-topic-each to uniform mush, which makes sense because \_\_\_\_\_" or "the `rm_top` I liked in Part I started removing 'lord' and 'love' here, so I \_\_\_\_\_" or "in 20NG about \_\_\_\_\_ of 20 topics were nameable subjects; in Shakespeare it was \_\_\_\_\_, and the rest were \_\_\_\_\_" or "my Shakespeare topics changed a lot between seeds while the 20NG ones mostly stayed put, and I think that is because \_\_\_\_\_"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_2 = rf"""
    {PLACEHOLDER}
    """
    return (answer_2,)


@app.cell
def _():
    # TODO: your preprocessing. Edit `normalize` and/or `vectorizer_v2`.
    # The next cell recomputes the statistics, and the form below re-tokenizes its documents with these two objects.
    def normalize(text):
        """Use optionally to run on the raw text before tokenization"""
        # text = text.replace("’", "'")    # <- curly apostrophe -> ASCII apostrophe
        return text

    vectorizer_v2 = CountVectorizer(
        strip_accents="unicode",
        lowercase=False,
        stop_words=None, # note: if you try "english,"" the list is lowercase, so it only removes "the", not "The", unless lowercase=True)
        token_pattern=r"(?u)\b\w+\b", # see above
        ngram_range=(1, 1), # feel free to try bigrams and beyond
        analyzer="word", # feel free to try subwords
    )
    return normalize, vectorizer_v2


@app.cell
def _(DOC_CFG, base_stats, normalize, stats_table, vectorizer, vectorizer_v2):
    # quantifying some effects of your preprocessing w/ the Part I vectorizer vs your preprocessing
    if vectorizer_v2.get_params() == vectorizer.get_params() and normalize("man’s") == "man’s":
        _out = mo.callout(mo.md("Change `normalize` or at least one `CountVectorizer` argument in the cell above to see what it does to the statistics."), kind="info")
    else:
        _yours = stats_table({f"{_k} (your preprocessing)": [normalize(_t) for _t in _v[0]] for _k, _v in DOC_CFG.items()}, vectorizer_v2.build_analyzer())
        _base = base_stats.drop(index="20newsgroups (post)").rename(index=lambda _s: f"{_s} (Part I vectorizer)")
        _compare = pd.concat([_base, _yours]).sort_index()
        _out = mo.vstack([
            mo.ui.table(_compare.drop(columns=["top_tokens"]).reset_index().rename(columns={"index": "documents"}), selection=None, pagination=False),
            mo.md("Top 10 tokens: " + "; ".join(f"**{_k}**: {_v}" for _k, _v in _compare["top_tokens"].items())),
        ])
    _out
    return


@app.cell
def _(ALL_DOCS, normalize, tokenize_cfg, vectorizer_v2):
    # tokenized (normalize + vectorizer_v2) to be trained on
    _analyzer_v2 = vectorizer_v2.build_analyzer()
    TUNE_DOCS = {_name: tokenize_cfg([normalize(_t) for _t in _texts], _meta, _analyzer_v2) for _name, (_texts, _meta) in ALL_DOCS.items()}
    mo.md("Documents the form can train on (your preprocessing, non-empty only): " + ", ".join(f"**{_k}** = {len(_v[0]):,}" for _k, _v in TUNE_DOCS.items()))
    return (TUNE_DOCS,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Training form from Part I (+ document def box)

    The controls below are the ones you used in Part I. "New random seed" adds a seed to a list and "Active seed" picks which one to use; the form holds the three vocabulary thresholds, `k`, `alpha`, `eta`, the "Fix alpha" box, and the number of training steps. Nothing trains until you press the form button. The one addition is the **Documents** box to specify which document definition to train on. Every option is tokenized with your current `normalize` + `vectorizer_v2` from the cell above, so preprocessing is one of the knobs here too

    Each trained model is kept in `model_history` together with its settings, and the active model is also available as `topic_model`. A seed you already trained with switches `topic_model` to that run without retraining; a new seed trains a new run with the current form settings. If you edit `normalize` or `vectorizer_v2`, the form resets and the documents are re-tokenized; the runs already in `model_history` stay (each remembers the documents it was trained on), so press the button again if you want a run on the new tokens. Every run is also appended to `model_history_part2.csv` next to this notebook the moment it finishes training; you will submit that file along with the notebook.
    """)
    return


@app.cell
def _():
    seed_selector = mo.ui.button(
        value=[random.randrange(2**31)],  # seed history; starts with one random seed
        on_click=lambda _v: _v + [random.randrange(2**31)],
        label="New random seed",
    )
    seed_selector
    return (seed_selector,)


@app.cell
def _(seed_selector):
    # The training cell below reads seed_picker.value.
    seeds_run = seed_selector.value
    seed_picker = mo.ui.radio(
        options={str(_s): _s for _s in seeds_run},  # one radio option per seed run
        value=str(seeds_run[-1]),                   # newest seed auto-selected
        label="Active seed",
        inline=True,
    )
    seed_picker
    return (seed_picker,)


@app.cell
def _(BASELINE_PT1Q2, TUNE_DOCS, train_lda):
    # All LDA settings except the seed in one form, starting from BASELINE_PT1Q2. Pressing the button trains one model.
    # This cell reads TUNE_DOCS and train_lda on purpose: if either changes (for example after an edit to normalize or
    # vectorizer_v2), the form is rebuilt with value None.
    _ = train_lda
    _b = BASELINE_PT1Q2
    def _snap(value, steps):   # a slider with fixed steps needs a value that is one of them
        return min(steps, key=lambda _s: abs(_s - value))
    _alpha_steps = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    _eta_steps = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0]
    lda_form = mo.ui.dictionary({
        "docs": mo.ui.dropdown(options=list(TUNE_DOCS), value="scene", label="Documents (which document definition to train on)"),
        "k": mo.ui.slider(start=2, stop=max(60, _b["k"]), step=1, value=_b["k"], show_value=True, include_input=True, label="Number of topics (k)"),
        "alpha": mo.ui.slider(steps=_alpha_steps, value=_snap(_b["alpha"], _alpha_steps), show_value=True, label="alpha (document-topic prior)"),
        "eta": mo.ui.slider(steps=_eta_steps, value=_snap(_b["eta"], _eta_steps), show_value=True, label="eta (topic-word prior)"),
        "fix_alpha": mo.ui.checkbox(value=False, label="Fix alpha at the slider value. Off: tomotopy re-estimates alpha during training, as in Part I"),
        "iters": mo.ui.slider(start=100, stop=max(5000, _b["iters"]), step=100, value=_b["iters"], show_value=True, include_input=True, label="Training steps"),
        "min_cf": mo.ui.number(start=0, stop=100000, step=1, value=_b["min_cf"], label="min_cf (drop tokens with total count below this)"),
        "min_df": mo.ui.number(start=0, stop=10000, step=1, value=_b["min_df"], label="min_df (drop tokens in fewer documents than this)"),
        "rm_top": mo.ui.number(start=0, stop=1000, step=1, value=_b["rm_top"], label="rm_top (drop this many most frequent tokens)"),
    }).form(submit_button_label="Train a model with these settings", bordered=True)

    mo.vstack([lda_form, mo.md("_The form starts at your `BASELINE_PT1Q2` values. Every run is kept in `model_history`. If you submit settings, documents and a seed you already trained, the notebook switches to that run instead of training again._")])
    return (lda_form,)


@app.cell
def _():
    model_history = {}   # every form run, label -> {"settings", "docs", "docs_data", "model", "trace"}

    # every model trained in this notebook (form runs and run_model calls) is also appended to this CSV, which you submit
    HISTORY_CSV = (mo.notebook_dir() or Path.cwd()) / "model_history_part2.csv"
    SESSION_STARTED = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_run(label, source, docs_name, settings, model, trace):
        """Append one row for a trained model: when, which documents, every setting, vocabulary counts, fit, and the training trace."""
        row = {
            "session started": SESSION_STARTED,
            "trained at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "run": label,
            "source": source,          # "form" or "run_model"
            "docs": docs_name,
            **{_k: settings.get(_k) for _k in ("k", "alpha", "eta", "fix_alpha", "iters", "min_cf", "min_df", "rm_top", "seed")},
            "n docs": len(model.docs),
            "distinct tokens seen": len(model.vocabs),   # before thresholds; changes only if the preprocessing changed
            "tokens kept": len(model.used_vocabs),
            "log-likelihood/word": round(model.ll_per_word, 3),
            "perplexity": round(model.perplexity, 1),
            "log-likelihood/word trace (step:value)": " ".join(f"{_t[0]}:{_t[1]:.3f}" for _t in trace),
        }
        pd.DataFrame([row]).to_csv(HISTORY_CSV, mode="a", header=not HISTORY_CSV.exists(), index=False)

    return HISTORY_CSV, log_run, model_history


@app.cell
def _(
    HISTORY_CSV,
    TUNE_DOCS,
    lda_form,
    log_run,
    model_history,
    seed_picker,
    train_lda,
):
    # Trains one model per (form settings, documents, active seed), files it in model_history, and appends a row to the CSV.
    if lda_form.value is None:
        topic_model, ll_trace = None, []
        _out = mo.callout(mo.md("Nothing trained yet. Set the values above and press the button."), kind="info")
    elif any(_v is None for _v in lda_form.value.values()):
        # a number field that was cleared with the keyboard arrives as None; tomotopy rejects None for
        # min_cf / min_df / rm_top and silently runs unseeded for seed=None
        topic_model, ll_trace = None, []
        _out = mo.callout(mo.md("Every field in the form needs a value. Fill in the empty one and press the button again."), kind="warn")
    else:
        _settings = dict(lda_form.value, seed=seed_picker.value)
        _docs_name = _settings.pop("docs")
        _same = [_l for _l, _r in model_history.items() if _r["settings"] == _settings and _r["docs"] == _docs_name]
        if _same:
            topic_model, ll_trace = model_history[_same[0]]["model"], model_history[_same[0]]["trace"]
            _out = mo.md(f"Switched to **{_same[0]}**. These settings, documents and seed were already trained, so nothing ran again.")
        else:
            _toks, _meta = TUNE_DOCS[_docs_name]
            topic_model, ll_trace = train_lda(docs=_toks, **_settings)
            _label = f"run {len(model_history) + 1}: docs={_docs_name} " + " ".join(f"{_key}={_val}" for _key, _val in _settings.items())
            model_history[_label] = {"settings": _settings, "docs": _docs_name, "docs_data": (_toks, _meta), "model": topic_model, "trace": ll_trace}
            log_run(_label, "form", _docs_name, _settings, topic_model, ll_trace)
            _out = mo.md(
                f"Trained **{_label}** in {ll_trace[-1][0]} steps on {len(_toks):,} documents. "
                f"Kept {len(topic_model.used_vocabs):,} distinct tokens; removed as top words: `{list(topic_model.removed_top_words)}`. "
                f"Appended to `{HISTORY_CSV.name}`."
            )
    _out
    return (topic_model,)


@app.cell
def _(show_topics, topic_model):
    mo.stop(topic_model is None, mo.md("_Train a model with the form above to see its topics here._"))
    show_topics(topic_model, top_n=12)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Model history (saved automatically; you will submit `model_history_part2.csv` with this notebook!)

    The table below shows every run from the form, with its settings and a few numbers. Every one of them was also appended to `model_history_part2.csv` next to this notebook the moment it finished training, as were the three Question 1 models, the 20 Newsgroups reference, and anything you train by hand with `run_model` (the `source` column tells them apart). It is okay if there are duplicate rows, e.g. from completing the assignment across several sittings. As in Part I, log-likelihood per word is only comparable between runs that kept the same vocabulary (same documents, same preprocessing, same thresholds); check the "tokens kept" column before comparing.
    """)
    return


@app.cell
def _(HISTORY_CSV, model_history, topic_model):
    _ = topic_model   # read so that this cell re-runs after every form run (model_history changes in place)
    mo.stop(not model_history, mo.md(f"_`model_history` is empty. Train a model with the form above. (Runs are written to `{HISTORY_CSV}`.)_"))
    _rows = [
        {
            "run": _l.split(":")[0],
            "docs": _r["docs"],
            **_r["settings"],
            "n docs": len(_r["model"].docs),
            "distinct tokens seen": len(_r["model"].vocabs),
            "tokens kept": len(_r["model"].used_vocabs),
            "log-likelihood/word": round(_r["model"].ll_per_word, 3),
            "perplexity": round(_r["model"].perplexity, 1),
            "active": "*" if _r["model"] is topic_model else "",
        }
        for _l, _r in model_history.items()
    ]
    mo.vstack([
        mo.ui.table(_rows, selection=None, pagination=False),
        mo.md(f"_Every run in this table was appended to `{HISTORY_CSV}` the moment it finished training. That file keeps the runs from earlier sittings too, and it is what you submit._"),
    ])
    return


@app.cell
def _(model_history, topic_model):
    # log-likelihood per word after every 100 steps, for every run in model_history
    _ = topic_model
    mo.stop(not model_history, mo.md("_Train a model with the form above to see its training curve._"))
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    for _label, _run in model_history.items():
        _ax.plot(
            [_t[0] for _t in _run["trace"]],
            [_t[1] for _t in _run["trace"]],
            marker=".",
            label=_label.split(":")[0] + f" ({_run['docs']}, k={_run['settings']['k']}, seed={_run['settings']['seed']}, iters={_run['settings']['iters']})",
        )
    _ax.set_xlabel("training steps")
    _ax.set_ylabel("log-likelihood per word")
    _ax.legend(fontsize=7)
    _fig
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Looking inside a document

    For a handful of documents, skim/read the documents that a given topic dominates. Pick a model and a document; the viewer shows where the document came from (play, scene, who speaks in it), its top topics in the matching model, and its text. For a given topic, try a few documents where that topic is on top.

    The dropdown lists the three Question 1 models (Part I vectorizer), every run you trained with the form (your preprocessing), and, once you have trained it, the 20 Newsgroups reference model.
    """)
    return


@app.cell
def _(
    ALL_DOCS,
    DOC_CFG,
    TOKENIZED,
    model_history,
    newsgroups_meta,
    newsgroups_model,
    newsgroups_texts,
    newsgroups_tokens,
    shakespeare_models,
    topic_model,
):
    # every model you can inspect -> (model, token lists, meta, raw texts)
    INSPECT = {f"Q1 {_k} (Part I vectorizer)": (_m, *TOKENIZED[_k], DOC_CFG[_k][0]) for _k, _m in shakespeare_models.items()}
    INSPECT.update({_l: (_r["model"], *_r["docs_data"], ALL_DOCS[_r["docs"]][0]) for _l, _r in model_history.items()})
    if newsgroups_model is not None:
        INSPECT["20 Newsgroups reference (BASELINE_PT1Q2, Part I vectorizer)"] = (newsgroups_model, newsgroups_tokens, newsgroups_meta, newsgroups_texts)
    _default = next((_l for _l, _v in INSPECT.items() if _v[0] is topic_model), "Q1 scene (Part I vectorizer)")   # follow the active form run
    model_picker = mo.ui.dropdown(options=INSPECT, value=_default, label="Model to inspect")
    model_picker
    return (model_picker,)


@app.cell
def _(model_picker):
    doc_slider = mo.ui.slider(start=0, stop=len(model_picker.value[1]) - 1, value=0, show_value=True, include_input=True, label="Document index")
    doc_slider
    return (doc_slider,)


@app.cell
def _(doc_slider, model_picker):
    _model, _toks, _meta, _texts = model_picker.value
    _j = doc_slider.value
    _dist = list(_model.docs)[_j].get_topic_dist()   # tomotopy 0.14.0 needs the list() before indexing past 0
    _top = sorted(range(len(_dist)), key=lambda _k: _dist[_k], reverse=True)[:5]
    _row = _meta.iloc[_j].to_dict()
    _text = _texts[_row["doc_id"]]   # raw (untokenized) text; doc_id indexes this definition's text list
    mo.vstack([
        mo.md(
            f"**{model_picker.selected_key}: doc {_j}** · " + " · ".join(f"{_c}: `{_row[_c]}`" for _c in _meta.columns if _c not in ("speakers", "doc_id"))
            + (f"\n\nspeakers: `{_row['speakers']}`" if "speakers" in _row else "")
            + "\n\ntop topics (id: prob, top words): "
            + "; ".join(f"**{_k}** ({_dist[_k]:.2f}: {', '.join(_w for _w, _p in _model.get_topic_words(_k, top_n=6))})" for _k in _top)
        ),
        mo.md(f"```\n{_text[:3000]}{'...' if len(_text) > 3000 else ''}\n```"),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### The 20 Newsgroups reference model (for Question 2, Part B)

    The cell below trains a 20 Newsgroups model, with `BASELINE_PT1Q2` and the Part I vectorizer, to compare with the Shakespeare model for Question 2b. Note that this cell is not affected by new model settings you try out above
    """)
    return


@app.cell
def _(
    analyzer,
    newsgroups_texts,
    newsgroups_train,
    run_model,
    show_topics,
    tokenize_cfg,
):
    # 20 Newsgroups reference model: trained with BASELINE_PT1Q2 and the Part I vectorizer
    _meta = pd.DataFrame({"doc_id": range(len(newsgroups_texts)), "newsgroup": list(newsgroups_train["label_text"])})
    newsgroups_tokens, newsgroups_meta = tokenize_cfg(newsgroups_texts, _meta, analyzer)
    newsgroups_model = run_model("20newsgroups / BASELINE_PT1Q2 / Part I vectorizer", newsgroups_tokens)
    _out = show_topics(newsgroups_model, top_n=12)
    _out
    return newsgroups_meta, newsgroups_model, newsgroups_tokens


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Question 3: Characters as documents (form and test a hypothesis)

    So far a document has been a play, a scene, or a speech. Now make it a character. `character_per_play` is all of one character's lines within one play: 1,556 documents with a median of about 115 tokens, but a long tail of tiny ones (the minimum is 1 token), so filter those out before you train. The form's Documents box already offers `character_per_play (>=50 tokens)`, and `keep_long` below lets you pick any other cutoff. `character_corpus` merges the same Folger id across plays (so Falstaff's three plays become one document; recall the id-reuse note above). Feel free to use the latter for further exploration.

    **Form one informal hypothesis about characters, design a topic-model test for it, run the test, and report what happened.** Fill in every blank of this frame:

    > I expect that character documents will [group / separate / share topics] according to \_\_\_\_\_ (play, genre, act, a label I assign such as status or role, how much they speak), because \_\_\_\_\_. I will test this by training a model on _____ documents (e.g. `character_per_play` (>=50 tokens), `character_corpus`, a custom `build_docs` split, a filtered subset of one of these doc definitions, or something else) with settings \_\_\_\_\_ and looking at \_\_\_\_\_ (a `topic_by` table, top words, per-document topic distributions, a corpus statistic). I will count the hypothesis as supported if \_\_\_\_\_. One thing that could fool me is \_\_\_\_\_.

    Then, in ~8 sentences plus one table or a few numbers: state the hypothesis; say exactly what you ran (documents, length filter, preprocessing, settings, seed); show the evidence; give a verdict (supported, not supported, or can't tell-- "can't tell" with a reason is a perfectly fine answer); say whether the confound you named was relevant; and say what you would try next.

    Tools to help are provided in cells below: `GENRE` maps each play to comedy / history / tragedy; `topic_by(model, meta, column)` cross-tabulates each document's dominant topic against any `meta` column (play, who, genre, act, or a column you add by hand), the same idea as `topic_by_newsgroup` in Part I; `keep_long(texts, meta, min_tokens)` drops short documents; `build_docs(speeches, [...])` makes any split the form does not offer, e.g. `["play", "act", "who"]` for character-by-act; `stats_table` works on any list of texts; `coherence_score` is copied from Part I with the same caveat.

    Example hypotheses: "a protagonist's topic mixture shifts between early and late acts"; "high-status and low-status characters differ in register, thou vs. you" (you will have to hand-label a dozen characters, which is allowed). Example *bad* hypothesis: "characters who talk more have lower within-document TTR" is true by construction, because TTR naturally falls with length
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_3 = rf"""
    {PLACEHOLDER}
    """
    return (answer_3,)


@app.cell
def _():
    # play code -> genre, by the three sections of the First Folio (1623). Per and TNK are not in the Folio; listed as comedies by convention.
    GENRE = {
        # comedies (14)
        "Tmp": "comedy", "TGV": "comedy", "Wiv": "comedy", "MM": "comedy", "Err": "comedy", "Ado": "comedy", "LLL": "comedy",
        "MND": "comedy", "MV": "comedy", "AYL": "comedy", "Shr": "comedy", "AWW": "comedy", "TN": "comedy", "WT": "comedy",
        # histories (10)
        "Jn": "history", "R2": "history", "1H4": "history", "2H4": "history", "H5": "history",
        "1H6": "history", "2H6": "history", "3H6": "history", "R3": "history", "H8": "history",
        # tragedies (12)
        "Tro": "tragedy", "Cor": "tragedy", "Tit": "tragedy", "Rom": "tragedy", "Tim": "tragedy", "JC": "tragedy",
        "Mac": "tragedy", "Ham": "tragedy", "Lr": "tragedy", "Oth": "tragedy", "Ant": "tragedy", "Cym": "tragedy",
        # not in the Folio (2)
        "Per": "comedy", "TNK": "comedy",
    }
    ROMANCES = {"Per", "Cym", "WT", "Tmp", "TNK"}   # the later, contested "romance" grouping, if you want a second label
    return


@app.cell
def _():
    def keep_long(texts, meta, min_tokens):
        """Drop documents with fewer than `min_tokens` whitespace-separated words. Returns (texts, meta), still aligned,
        with `doc_id` re-numbered so that it indexes the returned text list."""
        keep = [i for i, t in enumerate(texts) if len(t.split()) >= min_tokens]
        meta = meta.iloc[keep].reset_index(drop=True)
        meta["doc_id"] = range(len(keep))
        return [texts[i] for i in keep], meta

    def dominant_topics(model):
        """One entry per document in `model`: its single most probable topic, or None if every token was pruned."""
        out = []
        for doc in model.docs:
            if all(t == -1 for t in doc.topics):
                out.append(None)
            else:
                dist = doc.get_topic_dist()
                out.append(max(range(len(dist)), key=lambda t: dist[t]))
        return out

    def topic_by(model, meta, column):
        """Rows: values of `column` in `meta` (e.g. "play", "who", "genre", or a column you add). Columns: topic id.
        Cell: number of documents in that row whose single most probable topic is that column.
        `meta` must be the meta that goes with the documents `model` was trained on (same length, same order):
        for a form run that is model_history[label]["docs_data"][1]; for a Question 1 model it is TOKENIZED[name][1].
        Documents whose every token was pruned are skipped. For genre: meta["genre"] = meta["play"].map(GENRE) first."""
        dom = dominant_topics(model)
        if len(dom) != len(meta):
            raise ValueError(f"model has {len(dom)} documents but meta has {len(meta)} rows; pass the meta the model was trained on")
        keep = [i for i, t in enumerate(dom) if t is not None]
        return pd.crosstab(
            pd.Series([meta.iloc[i][column] for i in keep], name=column),
            pd.Series([dom[i] for i in keep], name="dominant topic"),
        )

    return


@app.function
# copied from pt 1
# coherence helper (Question 8 plumbing)
def coherence_score(model, metric="c_v", top_n=10):
    """Mean coherence over all topics, computed on the model's own documents.
    metric: "c_v", "c_npmi", "c_uci", or "u_mass". Higher = more coherent for all four.
    Caveat: the score depends on the vocabulary the model kept, so two models with different
    thresholds are not on exactly the same scale."""
    return Coherence(model, coherence=metric, top_n=top_n).get_score()


@app.cell
def _():
    # Commented out examples for Q3
    #
    # 1) a form run on character documents, cross-tabulated by genre (look up the run's label in the model history table):
    # _run = model_history["run 1: docs=character_per_play (>=50 tokens) ..."]
    # _meta = _run["docs_data"][1].copy()
    # _meta["genre"] = _meta["play"].map(GENRE)
    # topic_by(_run["model"], _meta, "genre")
    #
    # 2) the same by hand, with a stricter length filter and the Part I vectorizer:
    # _texts, _meta = keep_long(*character_per_play, 100)
    # _toks, _meta = tokenize_cfg(_texts, _meta, analyzer)
    # char_model = run_model("character-per-play >=100 / part1-vectorizer", _toks)
    # topic_by(char_model, _meta, "play")
    #
    # 3) a split the form does not offer, e.g. character by act:
    # _texts, _meta = build_docs(speeches, ["play", "act", "who"])
    #
    # 4) coherence_score(char_model)   # same caveat as in Part I: only comparable between models that kept the same vocabulary
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
