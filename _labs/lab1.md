---
title: "Lab 1"
nav_order: 1
points: 9
due: 2026-09-17   # Part 1 due 2026-09-11 (Friday); Part 2 (final) due 2026-09-17
---

**Part 1 is due Friday, September 11 at 11:59pm ET.**

In Part 1 you will set up a local `uv` environment, load and explore the [20 Newsgroups corpus](http://qwone.com/~jason/20Newsgroups/), and train and tune topic models on it. Nine questions, with demonstrations and scaffolding in between.
<!--more-->

## Starter notebook

[`lab1_pt1.py`]({{ '/assets/labs/lab1_pt1.py' | relative_url }})

## Required Deliverables

You will submit `lab1_pt1_yourandrewid.py` and `model_history_yourandrewid.csv`

The notebook appends every run to `model_history.csv` next to itself as soon as it finishes training. Please simply rename the file and submit it along with the notebook

## Recommended for running

`uv run marimo edit` for the browser interface (Clara does this), OR the marimo extension on VSCode (Sireesh does this)

## Allowed and recommended resources

- assistance from course staff
- provided scaffolding in starter notebook
- official documentation such as through `help(LDAModel)` and [the official page](https://bab2min.github.io/tomotopy/v0.14.0/en/)
- piazza Q&A (your own questions and/or others')
- other course materials (e.g. released in-class activities)
- internet for general resources to understand subject material
- speech-to-text to help transcribe answers

## Prohibited

- AI generated answers
- copying a friend's notebook

## Explicitly *not* required
- polished prose (complete sentences, grammar): for this assignment, we will evaluate written answers for thoughtful responses, which should be expressed clearly and precisely enough to be legible to your peers and instructors, but need not be in complete sentences of Standard English for full credit. e.g. if you would sometimes tend to use a dedicated grammar checker (or LLM) on your writing before submission, we would happily accept, and would actually prefer, the more "raw" version
- a perfect `model_history.csv`: Duplicate entries are perfectly alright (e.g. from completing the homework across multiple sittings and rerunning some cells). Even a couple missing entries should be okay. If you end up with a couple missing rows, it would be helpful to us if you could roughly describe what is missing, but no worries if not. If you end up with multiple `model_history.csv` files, please concatenate the rows to just one file for submission. We will use these csvs in an in-class activity after Assignment 1 is due