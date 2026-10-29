---
layout: default
title: "Rubric Design Activity"
permalink: /rubric-design/
---

# Rubric design activity

Together with your group, you will design rubrics for your course projects and eventually be assessed using the rubrics you design. By now, you should have a decent idea of your project's challenges and limitations, potential roadblocks, and valuable contributions and outcomes. Start from your proposals if helpful! We will provide a rough template, and some criteria will be fixed, but in general you will be responsible for describing specific rubric criteria as applicable to your specific projects.

For today's assignment, you will receive credit for making a good faith attempt at writing clear rubric criteria and eventually arriving at a rubric that you, your group members, and the instructors are happy with. You will not be penalized for being asked to iterate on an initial rubric. For each criterion, you will provide descriptions of what success looks like (for full credit), and optionally, what meeting "stretch" goals would look like (for full credit + up to 2 bonus points total), but you will only need to write a general statement of what could lead to falling short of goals, and how you plan to avoid these potential pitfalls. You will specify both group criteria and a small subset of individual criteria-- your final projects will be graded via self-assessment and instructor application of the rubrics you design today.

## What to submit
Format is flexible: Markdown, a Google Doc, or [COLM-style](https://www.overleaf.com/latex/templates/colm-2026-template/wbwzrwczsqvg) PDF are all fine.

* Proposed criteria: 6 to 8 criteria together worth 65% of the total project grade, with no single criterion worth more than 20%.
    * Proposed group criteria: 4-6 criteria, worth 45-60% of members' project grades
    * Proposed individual criteria: at least 1 and up to 2 criteria per member, worth 5-20% of that member's project grade. Individual criteria may cover work that the member owns and/or may generally apply to all members
* Pitfalls: general statement of what could lead to falling short of goals, and how you plan to avoid these potential pitfalls
* Justification: 1-2 paragraphs explaining why the rubric overall and its scope fits your group's existing skills and your planned AI use
* AI-use disclosure for this assignment, if you used AI (see below)
* Optional: a tentative week-by-week timeline. If you submit it, we give feedback on it, but your project will not be graded on whether you stick to it

### Template for each criterion
> - Name and weight:
> - Group or individual (if individual, which member):
> - Success (full marks): concrete, checkable outcomes of work you will do.
> - Stretch goal (optional. completing stretch goals earn up to 2 bonus points across the whole project):
> - Alternate or fallback path: if you run into issues with your main plan, what you'll do instead, and whether that earns full or partial marks
> - Risks and mitigation: a general statement of what could cause you to fall short, and how you plan to avoid it.
> - Evidence: where the evidence of success will be (report section, table in report, repo folder, appendix, etc.).

#### Example criterion:
> - **Name and weight:** Shared ownership of project progress and tasks, 10%
> - **Group or individual:** Group
> - **Success:** We hold a weekly meeting and keep short notes on decisions and task assignments. Any individual member will be able to write the final report's contributions statement describing what each member did
> - **Stretch:** Each member pairs with another on the part of the project tied to their stated learning goal, at least once.
> - **Risks and mitigation:** One thing we want to avoid is one person scrambling to combine everyone's independent work at the last minute. To try to prevent this, we'll set an internal deadline one week before the real one for a full draft.
> - **Evidence:** Commit history on the repo; contributions statement in final report.

#### Second example criterion:
> - **Name and weight:** Human validation of the automatic metric, 15%
> - **Group or individual:** Group
> - **Success:** We write annotation guidelines, have two members independently label 100 model outputs on a 1-5 quality scale, report inter-annotator agreement, and report the correlation between the human ratings and the automatic metric. We discuss what the correlation does and does not justify about the metric for our task.
> - **Stretch:** We run a second annotation round after revising the guidelines based on disagreements, and report how agreement changed.
> - **Alternate or fallback path:** If we fail to converge on guidelines, we run a 30-example pilot with open-ended notes and report the most common disagreements and what we learned, for partial credit (up to 12 of 15%).
> - **Risks and mitigation:** The label scheme may not fit the data. We will annotate 10 examples together first and revise the scheme before the full round.
> - **Evidence:** Guidelines in the repo under `annotation/`; agreement and correlation table in the Experiments section; the labeled Sheet linked from the appendix.

## Guidelines for writing criteria:
* Set guidelines based on things you have control over as a group! This can mean:
    * specifying multiple paths to full marks for a given criterion
    * defining success based on labor, effort, or milestones (e.g. "comparing ROUGE scores to human assessments of generated summaries via an annotation study of 100 doubly annotated examples for full marks" + "or running only a pilot study or open ended annotation if we fail to converge on a set of reasonable annotation guidelines" for partial credit), and avoiding definitions of success based on outcomes that you cannot predict ahead of time (e.g. "a ROUGE score of at least 0.45 will earn full marks, while 0.35-0.45 will earn partial marks")
* Specify criteria to be independent enough that they test different things (this also means you should try to limit obvious overlap with our base criteria)

### Fixed criteria (35%) will cover:
* clear, organized communication in the final report and presentation
* clearly defined, well-motivated problem and scope
* situation in related work
* documentation and reproducibility of implementations

Required sections: abstract, intro, related work, methodology, experiments and results, discussion and limitations

#### Things we would like you to assess but will leave to you to pick and define:
* specific project milestones and outcomes
* specific experiments and analyses
* quality checks on your work so far
* "successful" collaboration, whatever that looks like for your group

You may include things not on this list!

## AI use policy
* If you wish, you may use AI assistance to refine your rubrics, but only *after* you have thought through, discussed, and written down initial proposed rubric items as a group. You will be asked to submit your initial draft, describe any AI use, provide your inputs, and write a sentence or two on what changed as a result.
* You will be asked to justify your rubric in context of your group members' existing skillsets and your planned AI use. On AI use for the project itself, you are allowed! But do make sure you document and describe your AI use, including associated expected benefits and trade-offs
