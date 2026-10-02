---
title: "Lab 2"
nav_order: 2
points: 9
due: 2026-10-02   # Friday
---

**Due Friday, October 2 at 11:59pm ET.**

Lab 2 explores more involved ways to acquire data from the web and analyze it. Part I walks you through parsing a live webpage and sending requests via an API to gather a corpus, then an open-ended exploration of it. Part II points the same machinery at the source your project group actually means to use.

Note that for Part 2 of this lab, you will be working with your project groups to decide on a dataset to make, most likely relevant to your course project. Submissions will themselves be individual and to Canvas as before
<!--more-->

## Starter notebook

[`lab2.py`]({{ '/assets/labs/lab2.py' | relative_url }}). Part I and Part II are both in this one notebook.

## Data

Part I comes with a cached corpus as a dependency: [`olympic_extracts.jsonl`]({{ '/assets/labs/olympic_extracts.jsonl' | relative_url }}) (3.3 MB, 362 Wikipedia extracts; [provenance]({{ '/assets/labs/olympic_provenance.json' | relative_url }})). (You could extract these pages yourself, but the notebook assumes we provide a pre-cached set of plain-text article extracts.) Put it at `data/olympic_extracts.jsonl` next to the notebook, and launch marimo from that directory (e.g. `uv run marimo edit lab2.py`). The notebook reads `data/` relative to where you launched it

## What to hand in

Your completed lab 2 notebook, with all seven questions answered.

| | comes from | what |
|---|---|---|
| 1 | Part I | Questions 1 to 3, and the Part I data card |
| 2 | Part II | Questions 4 to 7, answered for your group's own source rather than the worked example |
| 3 | Part II | your blocker log and the Part II data card |

Part I is individual work. Part II is built with your project group, but the notebook and the writeup you submit are your own: you should be able to defend every cell you hand in

## Part I (individual, Questions 1 to 3)

Research question: *What kinds of multi-sport backgrounds do elite athletes have in their youth?* 

Corpus: the union of the three tables in Wikipedia's [List of multiple Olympic gold medalists](https://en.wikipedia.org/wiki/List_of_multiple_Olympic_gold_medalists)

- Question 1: Parser or API
- Question 2: Which issues do you choose to deal with?
- Question 3: What is still broken

You will need to write code in places containing `# TODO(student)`. Cells marked `[REUSABLE]` are portable HTTP plumbing that you should read to understand and feel free to borrow when you are completing Part II.

Five rules for automated traffic to servers paid for by someone else:

1. Know the license (Wikipedia text is CC BY-SA 4.0)
2. Identify your client: send a `User-Agent` naming the tool and a contact
3. Read `robots.txt` first
4. Go slowly, back off when told; honor `HTTP 429` and `Retry-After`
5. Cache everything; re-running a cell should not require additional requests

## Part II (group work, individual writeup, Questions 4 to 7)

Take the source your group actually means to use for the course project and build the first working slice of a pipeline against it. This is a proof of concept, not a finished dataset: build and test each piece (fetch, extract, structure, sample-check) against your real, messy source, and document where it fought back. A group that hits a real wall and documents it clearly scores as well as one whose source behaved perfectly; we assess the rigor of what you found, not how clean the corpus turned out.

If your group does not have a data source yet, the notebook includes four example sources as fallbacks: GitHub repos using PyTorch, NeurIPS paper checklists, SEC EDGAR 10-K risk factors, and the ACL Anthology.

- Question 4: Modality and cost
- Question 5: What counts as one document
- Question 6: What counting revealed
- Question 7: Hypothesis, result, verdict

This is group work! Choose the source and build the pipeline together. However, you should work in your own notebook and hand in your own writeup.

**Please attempt this work without AI coding assistance.** For a Post-Lab 2 activity we will ask you to reflect on an AI coding assistant's performance on the same task.

Every blocker ends in `fixed` or `deferred` (with an honest effort estimate and what it would unblock)

The data card: a reader who never saw your code should be able to tell, from the card alone, what your numbers are numbers of and what they cannot be used for. "Unknown, because ..." is acceptable, but you should fill out all cells
