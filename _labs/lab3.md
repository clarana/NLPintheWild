---
title: "Lab 3"
nav_order: 3
points: 9
due: 2026-10-30   # Friday
---

**Lab 3 is due Friday, October 30 at 11:59pm ET.**

Lab 3 is about data annotation and evaluation. In Part I you will study and (re-)annotate natural language inference task examples: draft validation instructions for the [MNLI](https://cims.nyu.edu/~sbowman/multinli/) corpus, pilot hypothesis creation and validation yourself, annotate 100 examples, and discuss your disagreements and agreement metrics with your group.

In Part II you will work with your project group to specify an annotation task of your own, tied to your course project: describe the task, draft v1 annotation guidelines, and pilot them with an LLM. In the Post-Lab 3 activity, another group will annotate your items using only your guidelines.

Both parts involve collaboration with your group members, but each student submits their own assignment to Canvas.
<!--more-->

## Starter notebook

[`lab3.py`]({{ '/assets/labs/lab3.py' | relative_url }})

## Plan your group work

Some questions depend on others, so planning early saves a lot of back-and-forth:

- **Tuesday, October 20 (in class):** annotation and agreement exercise. This is the validation part of Q4, and we will go over the agreement metrics you need for Q6.
- **Q1 → Q2:** everyone finishes Q1 before you merge instructions
- **Q4 and Q5 (solo) → Q6:** everyone finishes all 100 Q5 items before Q6
- **Q7 → Q8 → Q9:** the Q9 pilot needs your Q8 guidelines and an LLM run

You can do Q2 asynchronously in a shared doc (one person merges, the others approve) or in a short call. Q6 needs a live group session (roughly 30 to 45 minutes), and Part II needs 1 live session or so (roughly 45 to 60 minutes).

Some tips:

- plan your session dates ahead of time
- set an internal group deadline for Q5 that falls before your Q6 session
- do Q5 in one or two sittings (roughly 60 to 90 minutes per person)

## Questions

`[INDIVIDUAL]` answers must be your own writing (you may still discuss them with your group). `[GROUP]` answers may match your group members' verbatim.

**Part I: Exploring ambiguity and subjectivity in established annotation tasks**

1. Draft the validation instructions `[INDIVIDUAL]`
2. Group candidate prompt `[GROUP]`
3. What else shapes annotation results `[INDIVIDUAL]`
4. MNLI annotation pilot `[INDIVIDUAL]`
5. Annotate 100 examples each `[INDIVIDUAL]`
6. Discuss disagreements `[GROUP]`

**Part II: Specifying your own annotation task**

{:start="7"}
7. Design your own annotation task `[GROUP]`
8. Draft v1 annotation guidelines `[GROUP]`
9. Pilot your guidelines with an LLM `[GROUP]`

If your project's own annotation task isn't ready yet, the notebook lists four alternative / backup annotation tasks; ask course staff first if you want to adopt one.

**Optional bonus questions** (individual, up to 0.5 points each)

1. Build an annotation interface
2. NLI for your project
3. LLM-written MNLI hypothesis-creation instructions

## Required Deliverables

Submit to Canvas:

- the notebook, with every required answer cell filled in (bonus questions are optional)
- the header fields at the top of the notebook (name, Andrew ID, group, date) filled in
- a link to your group's annotation spreadsheet with view permission for CMU addresses (or at least the instructors'), pasted into your Q5 answer (or upload the spreadsheet with your submission)

## Annotation spreadsheet

For Q5, use the [lab3_annotation_sheet_template](https://docs.google.com/spreadsheets/d/1OtjGR-4Kf1osYpB_WLOa4C5RFBqKovk6ECd-ur6KZVw/edit?usp=sharing). Make one copy for your whole group (File > Make a copy) and work in the copy; it also computes the agreement metrics you will report in Q6. Each member works only in their own tab, and until everyone in your group has finished Q5, stay out of the `Summary` tab and other members' tabs. The notebook has the full setup instructions.

## Allowed and recommended resources

- assistance from course staff
- provided scaffolding in released materials for homework
- official documentation such as through `help()` and [dataset cards](https://huggingface.co/docs/hub/datasets-cards)
- piazza Q&A (your own questions and/or others')
- other course materials (e.g. released in-class activities)
- internet for general resources to understand subject material
- speech-to-text to help transcribe answers
- AI generated annotations for assignment components that explicitly instruct it
- sharing compute access with classmates (or asking instructors for assistance)
- sharing `[GROUP]` answers verbatim with group members

## Prohibited

- AI generated answers to assignment questions
- AI annotations for assignment components that call for manual (human) annotation
- copying a friend's notebook for individual answers

## Explicitly *not* required

- polished prose (complete sentences, grammar): for this assignment, we will evaluate written answers for thoughtful responses, which should be expressed clearly and precisely enough to be legible to your peers and instructors, but need not be in complete sentences of Standard English for full credit. e.g. if you would sometimes tend to use a dedicated grammar checker (or LLM) on your writing before submission, we would happily accept, and would actually prefer, the more "raw" version
- complete annotations for Part II
