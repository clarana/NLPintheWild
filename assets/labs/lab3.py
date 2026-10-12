import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo

    from datasets import load_dataset
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt


@app.cell
def _():
    # --- Fill in your info ---------------------------------------------------
    NAME = ""
    ANDREW_ID = ""
    GROUP = ""            # your project group, for Part II
    ASSIGNMENT = "Lab 3: Data Annotation and Evaluation"
    DATE = ""             # e.g. 2026-10-01

    _missing = [
        _k for _k, _v in [("NAME", NAME), ("ANDREW_ID", ANDREW_ID), ("DATE", DATE)]
        if not _v.strip()
    ]
    _header = mo.md(
        f"# {ASSIGNMENT}\n\n**Name:** {NAME or '(name)'}\n\n"
        f"**Andrew ID:** {ANDREW_ID or 'andrewID'}\n\n"
        f"**Group:** {GROUP or '(group name / names of members)'}\n\n**Date:** {DATE or '(date)'}"
    )
    _header if not _missing else mo.vstack([
        _header,
        mo.callout(mo.md(f"Header incomplete. Fill in: {', '.join(_missing)}"), kind="warn"),
    ])
    return


@app.cell
def _():
    QUESTIONS = {
        1: "[INDIVIDUAL] Draft the validation instructions",
        2: "[GROUP] Group candidate prompt",
        3: "[INDIVIDUAL] What else shapes annotation results",
        4: "[INDIVIDUAL] MNLI annotation pilot",
        5: "[INDIVIDUAL] Annotate 100 examples each",
        6: "[GROUP] Discuss disagreements",
        7: "[GROUP] Design your own annotation task",
        8: "[GROUP] Draft v1 annotation guidelines",
        9: "[GROUP] Pilot your guidelines",
    }
    BONUS = {
        1: "[INDIVIDUAL] Build an annotation interface",
        2: "[INDIVIDUAL] NLI for your project",
        3: "[INDIVIDUAL] LLM-written MNLI hypothesis-creation instructions",
    }
    PLACEHOLDER = "(write your answer here)"
    return BONUS, PLACEHOLDER, QUESTIONS


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Instructions

    Both Part I and Part II require collaboration with group members. However, each student should submit their own assignment. We will indicate components where students should each write their own responses (`[INDIVIDUAL]`), vs. questions where students should feel free to submit the exact same text as their group members (`[GROUP]`). You may discuss questions with your group even if a response is `[INDIVIDUAL]`.

    ### All answerable questions will be specified under h3 headers (like this one)

    The cell immediately following the question will contain the space to answer the question.

    ## Plan your group work

    Some questions depend on others, so planning early saves a lot of back-and-forth:

    - **Tuesday, October 20 (in class):** annotation and agreement exercise. This is the validation part of Q4, and we will go over the agreement metrics you need for Q6.
    - **Q1 -> Q2:** everyone finishes Q1 before you merge instructions
    - **Q4 and Q5 (solo) -> Q6:** everyone finishes all 100 Q5 items before Q6
    - **Q7 -> Q8 -> Q9:** the Q9 pilot needs your Q8 guidelines and an LLM run

    You can do Q2 asynchronously in a shared doc (one person merges, the others approve) or in a short call. Q6 needs a live group session (roughly 30 to 45 minutes), and Part II needs 1 live session or so (roughly 45 to 60 minutes).

    **Some tips:**

    - plan your session dates ahead of time
    - set an internal group deadline for Q5 that falls before your Q6 session
    - do Q5 in one or two sittings (roughly 60 to 90 minutes per person)

    The lab is due Friday, October 30. In the Post-Lab 3 activity, another group will annotate your items using only your guidelines.

    ## What to submit

    - this notebook, with every required answer cell filled in (bonus questions are optional)
    - the header fields at the top of the notebook (name, Andrew ID, group, date) filled in
    - a link to your group's annotation spreadsheet with view permission for CMU addresses (or at least the instructors'), pasted into your Q5 answer (or upload the spreadsheet with your submission)
    - `[GROUP]` answers may match your group members' verbatim, while `[INDIVIDUAL]` answers must be your own writing

    -----

    #### Allowed and recommended resources

    - assistance from course staff
    - provided scaffolding in released materials for homework
    - official documentation such as through `help()` and [dataset cards](https://huggingface.co/docs/hub/datasets-cards)
    - piazza Q&A (your own questions and/or others’)
    - other course materials (e.g. released in-class activities)
    - internet for general resources to understand subject material
    - speech-to-text to help transcribe answers
    - AI generated annotations for assignment components that explicitly instruct it
    - sharing compute access with classmates (or asking instructors for assistance)
    - sharing `[GROUP]` answers verbatim with group members

    #### Prohibited

    - AI generated answers to assignment questions
    - AI annotations for assignment components that call for manual (human) annotation
    - copying a friend’s notebook for individual answers

    #### Explicitly not required

    - polished prose (complete sentences, grammar): for this assignment, we will evaluate written answers for thoughtful responses, which should be expressed clearly and precisely enough to be legible to your peers and instructors, but need not be in complete sentences of Standard English for full credit. e.g. if you would sometimes tend to use a dedicated grammar checker (or LLM) on your writing before submission, we would happily accept, and would actually prefer, the more "raw" version
    - complete annotations for Part II
    """)
    return


@app.cell
def _(ANSWERS, BONUS, BONUS_ANSWERS, PLACEHOLDER, QUESTIONS):
    DONE, TODO = "✅", "⬜"  # literal glyphs: a backslash escape inside an f-string expression breaks on Python < 3.12
    _rows, _done = [], 0
    for _n, _title in QUESTIONS.items():
        _a = (ANSWERS.get(_n) or "").strip()
        _ok = bool(_a) and _a != PLACEHOLDER.strip()
        _done += _ok
        _part = "Part I" if _n <= 6 else "Part II"
        _rows.append(
            f"**{DONE if _ok else TODO} Question {_n} ({_part}): {_title}**\n\n"
            + (_a if _ok else "_not yet answered_")
        )

    _brows, _bdone = [], 0
    for _n, _title in BONUS.items():
        _a = (BONUS_ANSWERS.get(_n) or "").strip()
        _ok = bool(_a) and _a != PLACEHOLDER.strip()
        _bdone += _ok
        _brows.append(
            f"**{DONE if _ok else TODO} Bonus {_n}: {_title}**\n\n"
            + (_a if _ok else "_not attempted_")
        )

    mo.vstack([
        mo.md(f"## Answer sheet: {_done}/{len(QUESTIONS)} required written  ·  {_bdone}/{len(BONUS)} bonus attempted"),
        mo.callout(
            mo.md("Answers live in this notebook's code. Fill in each `answer_N` cell "
                  "below the question; re-run to refresh this sheet. Bonus questions are "
                  "optional (up to 0.5 points each) and do not count toward the required total."),
            kind="info",
        ),
        mo.md("\n\n---\n\n".join(_rows + _brows)),
    ])
    return


@app.cell
def _(
    answer_1,
    answer_2,
    answer_3,
    answer_4,
    answer_5,
    answer_6,
    answer_7,
    answer_8,
    answer_9,
):
    # marimo does not track in-place dict writes, so the registry is rebuilt here.
    ANSWERS = {1: answer_1, 2: answer_2, 3: answer_3,
               4: answer_4, 5: answer_5, 6: answer_6,
               7: answer_7, 8: answer_8, 9: answer_9}
    return (ANSWERS,)


@app.cell
def _(bonus_1, bonus_2, bonus_3):
    BONUS_ANSWERS = {1: bonus_1, 2: bonus_2, 3: bonus_3}
    return (BONUS_ANSWERS,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part I: Exploring ambiguity and subjectivity in established annotation tasks

    ## Corpus description

    In the first part of Lab 3, you will study and (re-)annotate examples from the Multi-Genre Natural Language Inference corpus ([MultiNLI](https://cims.nyu.edu/~sbowman/multinli/); [Williams et al., 2018](https://aclanthology.org/N18-1101/)), perhaps better known as MNLI since its inclusion in the General Language Understanding Evaluation benchmark ([GLUE](https://gluebenchmark.com/); [Wang et al., 2019](https://openreview.net/forum?id=rJ4km2R5t7)). (Though in 2026 GLUE is commonly considered "saturated" or "solved," it was originally released as "a tool for evaluating and analyzing the performance of models across a diverse range of existing NLU tasks," and once was widely used (along with others) as a key benchmark for evaluating "general" model capability, or as a proxy for the quality of the representations learned by a pre-trained model.)

    Natural Language Inference (NLI) itself, also known as Recognizing Textual Entailment (RTE), is a term used to refer to a type of text classification task in which a model is tasked with predicting whether a natural language sentence entails or contradicts (or neither!) a second sentence. MNLI was presented as a "challenge" corpus at a time when the Stanford Natural Language Inference corpus ([SNLI](https://nlp.stanford.edu/projects/snli/); [Bowman et al., 2015](https://aclanthology.org/D15-1075/)) was a prominent predecessor benchmark for NLI.

    The authors of the MNLI dataset description paper specify a procedure in Section 2 for bulk collection of premises, crowdsourced annotation to create candidate hypotheses from premises, and crowdsourced annotation to validate pairs. However, the details are not fully specified; in particular, the exact instructions and interface wording that annotators saw in the validation round are not reproduced in the paper. In Question 1 below, you will try to write these instructions yourself.

    We will ask you to load the MNLI dataset from the Hugging Face Hub [**[HERE]**](https://huggingface.co/datasets/nyu-mll/multi_nli) (code snippet provided below), though the "raw" release is also available on this [webpage](https://cims.nyu.edu/~sbowman/multinli/).

    ## Data sources and citations

    Q5 and Q6 use ChaosNLI (Nie, Zhou, and Bansal, "What Can We Learn from Collective Human Opinions on Natural Language Inference Data?", [EMNLP 2020](https://arxiv.org/abs/2010.03532)), which collected 100 human annotations each for 4,645 NLI examples (1,599 of them from MNLI). Per the authors' README, ChaosNLI is licensed under Creative Commons Non-Commercial 4.0 (CC BY-NC 4.0). We took the data from the Hugging Face mirror [earino/chaosnli](https://huggingface.co/datasets/earino/chaosnli). MNLI data has different licenses for different subsets of data; the dataset card notes:

    > The majority of the corpus is released under the OANC’s license, which allows all content to be freely used, modified, and shared under permissive terms. The data in the FICTION section falls under several permissive licenses; Seven Swords is available under a Creative Commons Share-Alike 3.0 Unported License, and with the explicit permission of the author, Living History and Password Incorrect are available under Creative Commons Attribution 3.0 Unported Licenses; the remaining works of fiction are in the public domain in the United States (but may be licensed differently elsewhere).
    """)
    return


@app.cell
def _():
    mnli_data = load_dataset("nyu-mll/multi_nli", split="validation_matched")
    mnli_data
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 1: Draft the validation instructions  `[INDIVIDUAL]`

    Carefully read the methodology section of the [MNLI paper](https://aclanthology.org/N18-1101.pdf). Notice that the authors describe two distinct rounds of annotation, **Hypothesis Collection** and **Validation**.

    Look at how the tasks are actually described. Note that there aren't exact details on prompt/interface in the paper for the validation annotation task. Take a stab at writing out instructions for it FIRST, before peeking. Then try comparing with the semi-official version found in Sam Bowman's dissertation in his description of SNLI's creation (note different domain grounded in image captions).

    1. Provide the instructions you wrote.
    2. Provide rationales behind the way you formed your instructions.
    3. *Now*, compare your approach to the semi-official version for SNLI. What differences and similarities do you note? Anything you think is more or less clear in the provided prompt or yours? Anything you think could lead to annotator disagreement?

    From Sam Bowman's dissertation (SNLI, similar task but different domain grounded in image captions): https://cims.nyu.edu/~sbowman/bowman2016phd.pdf

    **Write your own instructions FIRST, then open the box two cells below to compare.**
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_1 = PLACEHOLDER
    mo.md(answer_1)
    return (answer_1,)


@app.cell(hide_code=True)
def _():
    mo.accordion({
        "Click to reveal: the SNLI validation prompt from Bowman's dissertation": mo.md(r"""
    > The Stanford University NLP Group is collecting data for use in research on computer understanding of English. We appreciate your help! Your job is to figure out, based on the correct caption for a photo, if another caption is also correct:
    >
    > - Choose definitely correct if any photo that was captioned with the caption on the left would also fit the caption on the right. Example: "A kitten with spots is playing with yarn."/"A cat is playing."
    > - Choose maybe correct if the second caption could describe photos that fit the first caption, but could also describe sentences that don’t fit the first caption. Example: "A kitten with spots is playing with yarn."/"kitten is playing with yarn on a sofa."
    > - Choose definitely incorrect if any photo that could possibly be captioned with the caption on the left would not fit the caption on the right. Example: "A kitten with spots is playing with yarn."/"A puppy is playing with yarn."
    >
    > We have already labeled one out of every 250 HITs. Completing one of these HITs yields a bonus of \$1 for each response that matches our label for up to \$5
    """)
    })
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 2: Group candidate prompt  `[GROUP]`

    Now compare your instructions with your group members'. What things did you do differently and similarly? Take the best of all worlds and create a candidate prompt together. Provide it and explain the rationale behind it.
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_2 = PLACEHOLDER
    mo.md(answer_2)
    return (answer_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 3: What else shapes annotation results  `[INDIVIDUAL]`

    What information besides instructions might be relevant to the results of an annotation study? Think beyond the prompt text itself; but the SNLI prompt in the box above already hints at a couple of these. Write 5-7 sentences
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
    ### Question 4: MNLI annotation pilot  `[INDIVIDUAL]`

    Try 2 hypothesis creation tasks. Record how much time each took (in minutes). Any difficulties? Ambiguities? Confusions? Learning curve? Make a note of your reasoning when you aren't 100% sure of a hypothesis you are proposing or a label you are assigning. The validation part of the pilot is the in-class exercise on Tuesday, October 20; paste your in-class labels and times into the template below. Which did you find harder, creating hypotheses or validating pairs, and why?

    The two warmup premises below come from MNLI's `validation_matched` split. Please don't look up the original hypotheses for these premises in the dataset!

    **Hypothesis creation (2 premises x 3 hypotheses each):** for each premise, write three hypotheses: one that is definitely true given the premise (entailment), one that might be true (neutral), and one that is definitely false (contradiction), as in MNLI's **Hypothesis Collection** round

    For each premise, record roughly the time you took and your three hypotheses. Add brief notes explaining your reasoning wherever you weren't 100% sure.

    **Response template.** Adapt this template into your `answer_4` cell and fill it in in addition to the other parts of your answer. Leave each item's text as given.

    ```python
    r"\"\"
    ### Hypothesis creation

    **Premise 1** (travel): Despite a recent renovation, the Meadows Mall is the least appealing of the three suburban malls.

    - Entailment (definitely true):
    - Neutral (might be true):
    - Contradiction (definitely false):
    - Time (minutes):
    - Notes (anything you weren't 100% sure about):

    **Premise 2** (government): Over most of the 1980s and 1990s, the U.S. was able to invest more than it saved by attracting financing from abroad.

    - Entailment (definitely true):
    - Neutral (might be true):
    - Contradiction (definitely false):
    - Time (minutes):
    - Notes:

    ### In-class validation (Tuesday, October 20)

    - Paste your 20 labels from the class sheet (example_id: label), or a link to your tab:
    - Total time (minutes):
    - Items you were unsure about, and why:

    ### Follow-up

    - Difficulties / ambiguities / confusions / learning curve:
    "\"\"
    ```
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
    ## Annotation spreadsheet

    We are providing a spreadsheet for Q5 that you and your group members can fill out, which also computes the agreement metrics you will report in Q6: [**[lab3_annotation_sheet_template]**](https://docs.google.com/spreadsheets/d/1OtjGR-4Kf1osYpB_WLOa4C5RFBqKovk6ECd-ur6KZVw/edit?usp=sharing). To use it:

    - make one copy for your whole group (File > Make a copy) and work in the copy
    - each member works only in their own tab (`Member 1` to `Member 4`; feel free to rename them). Groups of fewer than 4 can leave the extra tabs blank (blank tabs are ignored)
    - `premise` and `hypothesis` are prefilled;
    - choose each label from the dropdown in the `label` column: entailment, neutral, or contradiction. Use the `notes` column for anything you want to flag
    - you do not need to type in the `Summary` or `README` tabs. `Summary` updates automatically, and `README` explains each metric
    - until everyone in your group has finished Q5, stay out of the `Summary` tab and other members' tabs!
    - when you are done, share the sheet with view permission for CMU addresses (or at least the instructors) and paste the link in your Q5 answer (or upload the spreadsheet with your submission)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 5: Annotate 100 examples each  `[INDIVIDUAL]`

    Now annotate 100 validation tasks each from ChaosNLI's MNLI subset. In order to simulate a semi-realistic annotation scenario, please refrain from checking each other's annotations as you are doing your own, and please do not feel like you should thoroughly double check your annotation work! Log your observations, thinking, complaints, etc. Did you do this all at once or in multiple sittings? Alone? Synchronously with group members? Did you start fatiguing at any point (when)? Would you do this work again for \$15? Paste the link to your group's spreadsheet (see the **Annotation spreadsheet** block above) in your answer, or indicate that you are providing a non-Sheets file instead

    **ChaosNLI:** [ChaosNLI](https://github.com/easonnie/ChaosNLI) ([Nie et al., EMNLP 2020](https://aclanthology.org/2020.emnlp-main.734/)) re-annotated existing NLI examples with 100 annotations per example (vs. 5 per MNLI pair after the Validation round), so each sentence pair has a much larger distribution of human labels. Your 100 pairs are the MNLI `matched` pairs from the validation set where only 3 of the original 5 annotators agreed on the label. Our pool deliberately mixes pairs where the ChaosNLI labels are near-unanimous with pairs where they split. During Q5, you will see only the premise and hypothesis. Do not look at or search for ChaosNLI labels (or the original MNLI gold labels). For spreadsheet setup, see the **Annotation spreadsheet** block above.
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
    ### Question 6: Discuss disagreements  `[GROUP]`

    Find 3 examples where there was disagreement and try to explain yourselves to each other.

    1. Report the agreement metrics provided and explain them in human words. Recall that we covered these metrics in class on October 20th. (Also report anything else you think might be interesting or relevant that the spreadsheet did not already calculate for you.) (2-5 sentences)
    2. Why did you disagree? Feel free to break down your answer by example. Did anyone make mistakes (note that this is acceptable for the purposes of this homework!! Mistakes happen in real annotations and are one of the multiple reasons why we often have multiple annotators per example)? Did you eventually come to an agreement? Did you decide any of the examples were genuinely ambiguous or subjective? (5-10 sentences)

    For item 1: the numbers will populate in the **Summary** tab of your group's spreadsheet. Feel free to use external resources to understand each metric. The overall metrics (percent agreement, Fleiss' kappa, Krippendorff's alpha) all measure different kinds of IRR (inter-rater reliability), i.e. how consistently different annotators give the same label to the same example.
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
    # Part II: Specifying your own annotation task

    In Part I, you (re-)annotated examples for a task that had already been fairly carefully specified. In Part II, you will work with your group to specify an annotation task of your own, tied to your course project: describe the task (Q7), draft guidelines for it (Q8), and pilot them (Q9). Two blocks below may help. **What counts as an annotation task?** sets out what we mean by the term, and **Alternative / backup annotation tasks** offers options if your project's own task isn't ready yet. Note that we don't expect a fully annotated dataset in Part II!!
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.accordion({
        "What counts as an annotation task?": mo.md(r"""
    For this assignment, we count something as an annotation task if it applies a defined label or judgment schema to a set of items, under written guidelines, so that a second person could in principle reproduce the labels\*. The expected output for this section is structured labels tied to items, plus the guideline.

    **In scope**

    - assigning a class from a fixed label set
    - pairwise or ranked preference on a stated criterion
    - marking and typing spans
    - rubric or scale scoring with written anchors
    - verifying or correcting machine-generated labels against a guideline
    - seeding or checking synthetic data, if a human makes a defined accept/reject or edit judgment per item
    - error-analysis labeling by a defined error type
    - qualitative coding of text, e.g. thematic or open coding of passages against a codebook, including a codebook you refine as you go\*

    **Borderline** (only with an added judgment step)

    - writing new examples from scratch, if each item then gets a defined quality or acceptance judgment
    - collecting or filtering data by a rule, if the rule is a human judgment per item (a mechanical filter doesn't count)

    **Out of scope**

    - pure scraping, downloading, or format conversion with no per-item judgment
    - model training or inference with no human or structured judgment step
    - ad hoc labeling with no written guideline

    **Minimum bar:** a defined schema, a written guideline, a set of items, and at least a small double-annotated subset so you can gain a sense of annotator agreement (though it may not be appropriate to calculate any specific agreement metric)

    \* For qualitative coding, "reproducing the labels" is in a looser sense. Codes can be *semantic* (the explicit surface meaning of a passage) or *latent* (an underlying idea or assumption that takes interpretation to see), and some traditions treat coding agreement as evidence that coders were trained alike rather than as validation. See Wikipedia pages on [thematic analysis](https://en.wikipedia.org/wiki/Thematic_analysis) (semantic vs. latent, inductive vs. deductive) and [coding in the social sciences](https://en.wikipedia.org/wiki/Coding_%28social_sciences%29).
    """)
    })
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 7: Design your own annotation task  `[GROUP]`

    (Recommended related [reading](https://www.cs.cmu.edu/~jbigham/posts/2014/half-workday-as-turker.html))

    Now try to come up with your own annotation task, relevant to your course project. Describe the task. Is it meant to be done by a human, a model, either, or both? If human annotators, who will they be? (Please come talk to us ASAP if you think you might want to publish anything you do here as research and you want to recruit annotators who are not group members! This may (or very well may not) warrant IRB approval, which takes time, or at least a proper check to see whether it would be required) What role does it play in your project? How many examples do you expect to need? What would make a "high quality" vs. "low quality" example? Any anticipated ambiguities you would like to mitigate?

    **_Note_**: We believe all groups will have some aspect of their project that would warrant *some* kind of annotation-- whether for seeding a synthetic data generation pipeline, evaluating the effectiveness of some pre-processing filter, creating an evaluation for a system that you are building, classifying failure modes of a system, qualitatively coding long form text or open-ended model responses, or something else. However, we recognize that e.g. some groups' projects may be structured such that a salient annotation task appropriate for this assignment is dependent on some initial work that may not be completed yet. In this case, we are happy to support your group by providing an alternative annotation task-- see below the answer cell immediately following
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_7 = PLACEHOLDER
    mo.md(answer_7)
    return (answer_7,)


@app.cell(hide_code=True)
def _():
    mo.accordion({
        "Alternative / backup annotation tasks": mo.md(r"""
        We have four alternative task descriptions you may decide to use:

        - **LLMBar-Natural instruction-following preference:** which of two outputs better follows an instruction; 60 to 94 pairs
        - **DynaSent Model-0 label check:** verify and correct a classifier's sentiment labels; 120 to 147 sentences
        - **Alpaca synthetic-record audit:** accept or reject synthetic training records; 50 to 100 records
        - **Argument spans and relations (Microtext):** detect, label, and link argument spans; 20 to 25 texts

        If you want to adopt one, ask course staff first; we can help you get set up with the data. Name it in Q7 and still answer every Q7 field for it. For the Microtext spans task, we don't expect agreement metrics, just a discussion of where you disagreed. Feel free also to adapt any of these toward your project!
        """)})
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Response template:** Adapt this template into your `answer_7` cell and fill it in in addition to the other parts of your answer. After the first line, the lines follow the Q7 questions above. Please answer each one explicitly; raw notes are fine. If you adopt a backup task, name it on the first line and still fill in every other line for that task. If any field does not apply to your data, say so and briefly state why

    ```python
    r"\"\"
    **Backup task adopted (if any):** (LLMBar, DynaSent, Alpaca, Microtext spans, or none)

    - **Task:** (the items, and what an annotator produces for each: a label, a preference, a score, spans, codes, an accept/reject decision, etc.)
    - **Human / model / either / both:** (pick one, and say why in one line)
    - **Annotators:** (if human: who they will be; for annotators outside your group, see the IRB note above)
    - **Role in our project:** (1-3 sentences: what the annotations feed into, e.g. seed data, a filter check, an eval set, failure-mode analysis)
    - **Number of examples:** (a rough count for your project, not this lab, in your unit: items, pairs, documents, spans, etc.; plus one line on why)
    - **High-quality example:** (one example, or a description of what makes one high quality)
    - **Low-quality example:** (one example, or a description of what makes one low quality)

    **Anticipated ambiguities** (add or remove lines as needed; one mitigation for each)
    - Ambiguity 1: (a case that annotators could read more than one way)
      - Mitigation: (e.g. a guideline rule, a worked example, an "unsure" option, adjudication)
    - Ambiguity 2:
      - Mitigation:
    - Ambiguity 3:
      - Mitigation:
    "\"\"
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 8: Draft v1 annotation guidelines  `[GROUP]`

    Come up with a v1 set of annotation guidelines for the task-- you may do this however you wish! For example, you may work on it individually and compare, collaborate and iterate synchronously, start with an LLM-generated backbone and edit it, or some combination of these options.  Regardless, please **document your process** and share below what you did-- what criteria were you using to iterate? Did you pilot anything? If you used AI at any point, what prompt did you give it? Please share your annotation guidelines. Also please share observations from along the way about shared assumptions, differences in individual assumptions that ended up surfacing through this process, differences in how you were approaching the problem, etc.

    Check below the answer cell for a response template.
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_8 = PLACEHOLDER
    mo.md(answer_8)
    return (answer_8,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Response template** Adapt this template into your `answer_8` cell and fill it in. Keep Part A, the guidelines themselves, to about one page (roughly 400 to 600 words). Part B holds your process notes and observations. Bullets and raw notes are fine in both parts. Rename or drop any heading that doesn't fit your task (e.g. trim the long "Labels / codes / ..." heading to whatever your schema uses). If qualitative coding, your codebook can be a living document that you keep refining as you code.

    ```python
    r"\"\"
    ### Part A: Guidelines v1

    #### Task in one sentence
    (what annotators do, to which items, and why)

    #### Unit of annotation
    (what one item is, e.g. a sentence, a response pair, a document, a passage, a model output)

    #### Labels / codes / scale / span and relation types
    (one entry per label, code, scale point, or span/relation type; for a pairwise or accept/reject task, also state the criterion)

    - (name): (definition, one or two lines). Decision rule: (when to choose it over the closest alternative)
    - (name): (definition). Decision rule:

    #### Worked examples
    (at least one per label, or per code family: the item or a pointer, the annotation, and a one-line reason)

    - Example 1:
    - Example 2:

    #### Edge cases and tie-break rules
    (known hard cases, and which rule wins when two labels or rules seem to apply)

    - (case): (what to do)

    #### What to do when unsure
    (e.g. pick a default, mark "unsure", or skip the item; say which, and where to leave a note)

    ### Part B: Process notes

    Be precise but don't be afraid to be brief!
    - How we produced the guidelines: (individually and compared / synchronously / LLM backbone then edited / combination)
    - Criteria we used to iterate: (what made you change a definition or a rule)
    - Pilots run (if any): (on which items, and what changed afterward)
    - AI prompts used (verbatim, if any):
    - Shared assumptions and individual assumptions that differed:
    - Differences in approach:
    "\"\"
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 9: Pilot your guidelines with an LLM `[GROUP]`

    Given your set of annotation guidelines from Q8 above, complete at least 3 example annotations (you can/should pilot more if you already have data and/or it's a "simple" task), by prompting an LLM of choice. State which AI system/model you used! Any considerations beyond availability and performance? (e.g. not wanting to send sensitive information to a for-profit company's server) Any issues? If you intend for your annotation task to eventually be performed by human annotators instead of or in addition to an AI model, describe any expected limitations of an AI system-- e.g. describe any disagreements you observe between your own group members on these items. **Sneak peek:** In the Post-Lab 3 activity, another group will annotate your items cold, using only your guidelines!

    See below the answer cell for a response template
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_9 = PLACEHOLDER
    mo.md(answer_9)
    return (answer_9,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Response template:** Adapt this template into your `answer_9` cell and fill it in. Copy an Item block for each extra item you pilot. Bullets and raw notes are fine.

    ```python
    r"\"\"
    - **Task:** (brief description)
    - **Schema:** (your labels, scale, span types, or codes, in one line)
    - **AI system / model:** (the tool or API, and the model name and version)
    - **Model selection considerations:** (any notes behind why you chose)
    - **Prompt:** (verbatim; or if you gave it your Q8 guidelines, say so and paste only what you added)

    **Item 1:** (the item text, or a pointer to it: an id, URL, or row number)
    - LLM annotation:
    - Notes from our group:

    **Item 2:**
    - LLM annotation:
    - Notes from our group:

    **Item 3:**
    - LLM annotation:
    - Notes from our group:

    **Issues, notes, and limitations:** (e.g. unclear guideline rules, items that fit no label, LLM output being good or odd, differing opinions about it among group members, expected differences between LLM and human annotator outputs)
    "\"\"
    ```
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Optional bonus questions

    Each is individual and worth up to 0.5 points.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Bonus 1: Build an annotation interface

    Create an interface for annotation in your own task. You may use AI tools and/or "vibecode"! Your interface need not be entirely custom either-- it can be another spreadsheet or built on another platform, for example. Try using it and critique it. What was your procedure? What tool(s) did you use? What do you like? What would you change?
    """)
    return


@app.cell
def _(PLACEHOLDER):
    bonus_1 = PLACEHOLDER
    mo.md(bonus_1)
    return (bonus_1,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Bonus 2: NLI for your project

    How could an AI system that is good at NLI be useful for your project? Describe the use case and, if applicable, the pipeline or system surrounding the NLI use case. Discuss why it might be appropriate. Are there any limitations you might anticipate? Any alternatives you would want to consider before actually committing?
    """)
    return


@app.cell
def _(PLACEHOLDER):
    bonus_2 = PLACEHOLDER
    mo.md(bonus_2)
    return (bonus_2,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Bonus 3: LLM-written MNLI hypothesis-creation instructions

    Have an LLM try and make up instructions for hypothesis creation for each of the genres in MNLI (the five genres in the matched split). Critique them. What model/system did you use? What issues do you think could come up? Do you think hypothesis creation would be easier or harder for any genres in particular?
    """)
    return


@app.cell
def _(PLACEHOLDER):
    bonus_3 = PLACEHOLDER
    mo.md(bonus_3)
    return (bonus_3,)


if __name__ == "__main__":
    app.run()
