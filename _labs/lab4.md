---
title: "Lab 4"
nav_order: 4
points: 9
due: 2026-11-20   # Friday
---

**Lab 4 is due Friday, November 20 at 11:59pm ET.**

Lab 4 is about language model inference and adaptation. In Part I you will work through a shared task, detecting and neutralizing biased language in Wikipedia edits from the [Wiki Neutrality Corpus](https://arxiv.org/abs/1911.09709).

In Part II you will identify the language model tasks in your course project and plan an approach for each, then take one of them a step further on your own.

Part II involves collaboration with your group members, and discussion with other group members is allowed throughout all parts of the lab, but each student will submit their own assignment to Canvas.
<!--more-->

## Starter notebook

[`lab4.zip`]({{ '/assets/labs/lab4.zip' | relative_url }}) (about 11 MB). It contains the notebook `lab4.py`, the prepared data, and two helper scripts; see `README.md` for setup.

## Setup

Lab 4 needs one new package in your course environment: `uv add anthropic` (or `pip install anthropic`). It also needs two keys: copy `.env.example` to `.env` in the Lab 4 folder and fill in the course key (posted on Piazza) and your Anthropic API key. If you don't have an Anthropic API key, send us a private Piazza message. Never paste a key into the notebook (or into your conversations with an AI agent)! Launch marimo from the Lab 4 folder (e.g. `uv run marimo edit lab4.py`).

The Claude runs for the whole lab should cost a few dollars at most; the notebook shows each run's estimated cost.

## Plan your work

Before starting, read Wikipedia's [neutral point of view policy](https://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view) and skim sections 1 to 3 of [Pryzant et al. (2020)](https://arxiv.org/abs/1911.09709).

- **Q6:** start bert-mini training first! In a terminal in the Lab 4 folder, run `python train_bert.py --seeds 0 1 2`. This should run fairly quickly on a machine with even a small GPU and takes just a few minutes on a recent MacBook, but may take up to about 30 minutes on an older CPU-only laptop. Either way, running this script first lets training run in the background while you work on Questions 1 to 5.
- **Q5 and Q7:** the course model (`qwen3-8b-wnc`) runs on a server that sleeps after 10 minutes without requests and takes about 2 minutes to wake, so click **Wake / check both endpoints** in the notebook a few minutes before your first run with it

## Questions

`[INDIVIDUAL]` answers must be your own writing (you may still discuss them with your group). `[GROUP]` answers may match your group members' verbatim.

**Part I: Exploring a shared task**

1. Warm-up: what does a neutralizing edit look like? `[INDIVIDUAL]`
2. One-token classification on a fixed budget `[INDIVIDUAL]`
3. A workload whose lengths you have to look up `[INDIVIDUAL]`
4. Training memory for `qwen3-8b-wnc` `[INDIVIDUAL]`
5. Which model, and what does it take to make it work? `[INDIVIDUAL]`
6. Better and worse training settings `[INDIVIDUAL]`
7. Generate and evaluate neutral rewrites `[INDIVIDUAL]`

**Part II: Language model tasks in your project**

{:start="8"}
8. Identify tasks `[GROUP]`
9. Choose an approach `[GROUP]`
10. One step further `[INDIVIDUAL]`

## Required Deliverables

Submit to Canvas:

- the notebook, with every answer cell filled in
- the header fields at the top of the notebook (name, Andrew ID, group, date) filled in
- a zip of your `lab4_runs` folder, which holds the records of your model runs (don't submit `lab4_ckpts`, which holds trained model weights, or your `.env`)

## Allowed and recommended resources

- assistance from course staff
- provided scaffolding in released materials for homework
- official documentation such as through `help()` and [dataset cards](https://huggingface.co/docs/hub/datasets-cards)
- piazza Q&A (your own questions and/or others')
- other course materials (e.g. released in-class activities)
- internet for general resources to understand subject material, including looking up GPU and API prices
- speech-to-text to help transcribe answers
- running language models through the notebook wherever a question asks you to (Questions 5, 7 and 10)
- AI assistance with setup and debugging only (installing packages, configuring your `.env`, fixing errors), not for writing or computing your answers
- sharing compute access with classmates (or asking instructors for assistance)
- sharing `[GROUP]` answers verbatim with group members

## Prohibited

- AI generated answers to assignment questions, including the calculations in Questions 2 to 5
- copying a friend's notebook for individual answers

## Explicitly *not* required

- polished prose (complete sentences, grammar): for this assignment, we will evaluate written answers for thoughtful responses, which should be expressed clearly and precisely enough to be legible to your peers and instructors, but need not be in complete sentences of Standard English for full credit. e.g. if you would sometimes tend to use a dedicated grammar checker (or LLM) on your writing before submission, we would happily accept, and would actually prefer, the more "raw" version
