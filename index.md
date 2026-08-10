---
layout: default
title: Home
nav_order: 1
---

# Interdisciplinary NLP: Language Modeling in the Wild

**Fall 2026** &nbsp;·&nbsp; Tuesdays & Thursdays, 12:30–1:50pm &nbsp;·&nbsp; Wean Hall 6403

**Instructors:** [Emma Strubell](https://strubell.github.io), [Clara Na](https://clarasna.com/), and [Sireesh Gururaja](https://siree.sh/)

---

### Table of Contents
- [Interdisciplinary NLP: Language Modeling in the Wild](#interdisciplinary-nlp-language-modeling-in-the-wild)
    - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Who are you?](#who-are-you)
    - [Logistics](#logistics)
  - [Topics](#topics)
    - [Part 1: Text as data and language technologies](#part-1-text-as-data-and-language-technologies)
    - [Part 2: Navigating tools and affordances](#part-2-navigating-tools-and-affordances)
    - [Part 3: Data curation and evaluation](#part-3-data-curation-and-evaluation)
    - [Part 4: Adapting models to domains](#part-4-adapting-models-to-domains)
  - [Schedule](#schedule)
  - [Assignments](#assignments)
    - [Labs and project](#labs-and-project)
    - [Reflections](#reflections)
  - [Policies](#policies)






## Overview

Recent advances in natural language processing (NLP), primarily powered by large language models (LLMs) show great potential for enabling advanced analysis of unstructured and semi-structured documents across a diverse array of applications – from accelerating scientific discovery by automatically analyzing materials science research literature, to facilitating a study of the evolution of narrative arcs in 20th century literature.

Historically, successful real world deployment has often required deliberate adaptation: careful definition of the task, curation of new or existing datasets, experimentation to identify strengths and limitations of existing off-the-shelf affordances, and/or consideration of computational and financial feasibility. On the other hand, recent developments in language technologies have included both 1) meaningful capability improvements in many settings that until recently were outside the scope of existing tools, and 2) lowered barriers to use and adaptation of language technologies.

In this class, students with concentrations outside of NLP (e.g. degree programs in materials science, English, …) and students with concentrations in or near NLP (LTI, MLD or equivalent expertise) will work with and learn from each other, to characterize and bridge gaps between the promise of modern language technologies and the successful deployment of these tools for real-world applications. Together, students will explore:

- Technical foundations for using language technologies, AI literacy and effective science communication;
- Identifying strengths and limitations of various approaches for adaptation to a specific domain or setting, and;
- Acquiring and curating data appropriate to a specific task or evaluation;
- Devising and executing a plan to accomplish research and analysis tasks given a goal.

### Who are you?

This class is likely a good fit for you if either of the following descriptions apply to you.

**Group A**: You are a student in a discipline outside of ML/NLP (e.g. a sufficiently different discipline within computing such as programming languages, or an entirely separate discipline such as English, biology or design), and you are interested in using language technologies (e.g. machine learning with text data, LLMs) for your work. You do not need to have a specific use case yet— part of the course's objective will be to refine a research question in the context of available resources and technology. However, you should have an understanding in general of what it looks like to do research in your discipline

**Group B**: You are a student "in NLP" i.e. actively engaged in NLP research through LTI faculty and/or coursework or similar, and interested in any or all of: 1) interdisciplinary research and communication, 2) domain adaptation and generalization, especially in practice, and 3) understanding common gaps between research and practice. You do not need to have a specific domain of interest yet, but you should be open to working with domain experts to accomplish a shared goal.

There may be other, more appropriate courses for you if:

- You are more interested in a general survey of data science and statistical analysis tools; this course has an explicit emphasis on **text as data.**
- You are more interested in a general introduction to NLP (take 11-611 or 11-711), without having a specific domain or tentative domain-specific goal in mind. (That being said, 11-611/711 is *not* a prerequisite for this course.)

**A note on programming experience.** Previous programming or coding experience is greatly helpful, but not a strict requirement. For example, students who have experience using statistical analysis software but have not spent time writing scripts or programs themselves may find the material approachable. It is explicitly not a requirement that you have completed a degree in computing or significant computational coursework, but all students will be expected to write code and conduct quantitative analyses throughout the course. We plan to support learning of the same throughout the semester. Both course staff and willing students will be available to assist with some challenges such as debugging software installations. If you are unsure of whether this course is fit for you, please feel free to contact the instructors!

A detailed syllabus is forthcoming. Please feel free to reach out to the instructors with any questions in the meantime!

### Logistics

| | |
|---|---|
| **Lecture** | Tuesdays & Thursdays, 12:30–1:50pm, Wean Hall 6403 |
| **Office Hours** | TBD |
| **Canvas** | TBD |
| **Piazza** | TBD |
| **Contact** | Please use Piazza for questions. For private matters, make a private post on Piazza and/or email the instructors. |

## Topics

In this course, students will do natural language processing "in the wild" to conduct research in a specialized domain: they will build a text-based dataset, measure and make claims about their data, and adapt language technologies to their dataset.

### Part 1: Text as data and language technologies
Students will begin by exploring general techniques and tools for analyzing text as data. Students will consider a historical perspective of natural language processing, learning about assumptions and tools for language processing that have evolved throughout the years, as well as underlying paradigms and constraints that have persisted even as our methods and surroundings have shifted.

Students will implement and compare various ways to encode language and text as information that one can study with a computer; by the end of the unit, students will be familiar with common use cases and limitations of methods for exploratory text data analysis, spanning command line tools, programming language-native functions, off-the-shelf libraries for natural language processing, and custom implementations. In particular, students will gain an understanding of differences in common methods and assumptions’ relevance across different settings; certain differences in domain or motivation may simply call for adjusted hyperparameters, while others may warrant entirely different toolsets or additional processing of text.

Examples of concepts and tools students will encounter:
- How to represent and model language, and at what level?
  - Bytes, subwords, words, sequences, documents, and corpora
  - Syntax, semantics, and discourse
  - Vectorized representations of language such as bag-of-words representations (unweighted, weighted), static word embeddings (e.g. GloVe), contextual word embeddings (e.g. BERT)
  - Graph representations of language such as dependency parses and HTML
- Processing language given a representation
  - Finding and/or transforming text using regular expressions, string functions, fuzzy matching, and Unix commands such as jq, sed, and grep
  - Tagging language with predetermined labels (e.g. named entity recognition or sequence classification), or describing language in relative terms (e.g. LDA topic models)


### Part 2: Navigating tools and affordances
In the second section, students will build their own corpus. Throughout, students will repeatedly confront the challenge of determining 1) what work needs to be done, 2) what tools already exist for performing this work, and 3) how well-suited existing tools are. In general, students will practice thinking about data, algorithms, metrics, settings, models, software, and hardware as affordances they may consider for off-the-shelf use to achieve some or even most aspects of their goals. 

Examples of concepts and tools students will engage with:
- Data storage and navigation (e.g. search engines, ElasticSearch, BM25, RAG embeddings)
- The World Wide Web and Internet (e.g. APIs, web scraping, network protocols)
- Large language models, MCPs, and agents
- Data governance (e.g. licenses, filters, provenance, privacy)

### Part 3: Data curation and evaluation
In the next section, students will choose appropriate evaluation protocols, assess the quality and suitability of evaluation protocols themselves, and both specify and perform data annotation labor as they consider ways to answer their specific research questions.

Examples of concepts and tools students will engage with:
- Annotation tasks and labor
- Measures of annotator agreement
- Benchmarks, metrics, and metric validity and reliability
- Quantitative and qualitative analysis
- "In domain" vs out-of-distribution data

### Part 4: Adapting models to domains
In the final section of the course, students will consider and try various methods for adapting existing models to their use cases, with a deep focus on LLMs. Methods discussed will span light-weight context augmentation (e.g. in-context learning), resource-intensive pre-training from scratch, and many techniques in-between. Notably, techniques do not fall along a universal one-dimensional scale in either cost or complexity. 

Examples of concepts and tools students will engage with:
- In-context adaptation (e.g. few-shot learning, system prompts, agent skills, retrieval augmented generation)
- Parametric adaptation (e.g. supervised fine-tuning, “mid-training”, reinforcement learning, offline or online model merging)
- Synthetic data generation 
- Lifelong / continual learning


## Schedule

Dates are tentative and subject to change. Readings and materials will be posted as the semester progresses.

<table>
  <thead>
    <tr><th>Week</th><th>Date</th><th>Topic</th><th>Materials</th></tr>
  </thead>
  <tbody>
  {% for s in site.data.schedule %}
    <tr>
      <td>{{ s.week }}</td>
      <td>{{ s.date | date: "%a %b %-d" }}</td>
      <td>{% if s.no_class %}<em>{{ s.topic }}</em>{% else %}{{ s.topic }}{% endif %}</td>
      <td>{% if s.slides %}<a href="{{ s.slides | relative_url }}">slides</a>{% endif %}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>

## Assignments

Grades are based on a combination of individual and group work.

| Component | Weight |
|---|---|
| Reflections | 20 |
| Introductory Presentations | 8 |
| Labs | 36 |
| Project | 36 |

**Reflections (20 points).** (6 assignments; 4 points each. Lowest grade dropped. Individual.) Reflections are meant to encourage engagement in and reflection on class lectures, especially with respect to goals and interests the student originally entered the class with. Specific prompts and questions will vary from reflection to reflection. More details below and in class.

**Introductory Presentations (8 points).** (1 assignment. Individual.) Students introduce themselves and their research interests. NLP students sign up to present on their own work and/or an adaptation method they are familiar with, and non-NLP students sign up to present on their own work and/or a dataset they are hoping to work with. All students identify goal(s) they are hoping to accomplish in taking the course. These introductory presentations will help students form teams for later labs and the course project.

**Labs (36 points).** (4 assignments; 9 points each. First lab is individual, the rest are group.) Labs are implementation- and analysis-heavy assignments (mostly Python/PyTorch) designed to give hands-on experience implementing the methodologies discussed in class. After the first lab, labs will be group assignments to be completed with project teams using the codebase being developed for your course project. All labs will have "tracks" or components for NLP students and non-NLP students.

**Project (36 points).** (Group.) A semester-long 2-4 person team project focused on carrying out a research goal within a particular domain of interest to people in a non-NLP discipline. There will be intermediate assignments and exercises (project proposal, project sharing, writing abstracts for each other's publication audiences) as well as a final presentation and report. More details below and in class.

### Labs and project
{% assign labs = site.labs | sort: "nav_order" %}
{% for lab in labs %}
<div class="assignment-summary">
  <h4 style="margin-bottom:.2em"><a href="{{ lab.url | relative_url }}">{{ lab.title }}</a> <small>— {% if lab.due %}due {{ lab.due | date: "%b %-d, %Y" }}{% else %}due TBD{% endif %}{% if lab.points %}, {{ lab.points }} pts{% endif %}</small></h4>
  {{ lab.excerpt }}
</div>
{% endfor %}

### Reflections

Throughout the semester, students will be asked to submit short written reflections based on ongoing work they have done for the class, through in-class activities, lab assignments, and course project work. Specific formats will vary, but many reflections will mirror the following format:

Given a language technology discussed in class, that you used during an assignment or in your project,
  1. what are some things you initially imagined it could be useful for?
  2. what are some limitations you imagined you would encounter? and
  3. after using the technology, how well did the technology's empirical performance align with or diverge from your hypothesized strengths and limitations? (+ bonus, propose alternative ways to address the limitations)

<!-- - Within the first two weeks of class, students are asked to individually define something they are hoping to accomplish given some data they may or may not already have. Initial reflections should consist of:
  - a broad objective (where students are already fairly certain that some subset or modified version of it should be feasible)
  - A, B, and C goals where feasibility and tractability are increasingly uncertain, and
  - an imagined concrete plan for accomplishing each of the goals to the best of their knowledge
  - (Optional / bonus in initial reflection, required thereafter): estimation of the costs of accomplishing these goals, in time, money, and/or other relevant considerations
- Two times during the remainder of the semester, students are asked to submit updated reflections:
  - revisit the original reflection, adjusting plans and/or goals as necessary, and coming up with more informed estimates of relevant resource costs.
  - reasess feasibility and tractability of the original A, B, and C goals
  - revise the previously proposed concrete plans to accomplish these goals (or a necessary modification of the goals), given new knowledge about language technologies and their strengths and limitations
  - make more informed estimates of relevant time/money costs
- Two times during the middle of the semester, students will submit explorations of the "inverse" inquiry throughout the semester: Given some language technology discussed during class,
  1. what are some things you imagine it could be useful for?
  2. what are some limitations you imagine you would encounter? and
  3. empirically test some of the hypothesized strengths/limitations of the technology (+ bonus, propose alternative ways to address the limitations and/or talk about tradeoffs of each method)
- The final reflection is tied to the project and the overall experience of participating in the class alongside students with considerably different disciplinary backgrounds. -->

## Policies

**Late Work:** TBD

**Academic Integrity:** TBD

**Accommodations:** Students with disabilities who require accommodations should contact the [Office of Disability Resources](https://www.cmu.edu/disability-resources/) and notify the instructors early in the semester.

**Wellness:** Take care of yourself. CMU offers support through [Counseling &amp; Psychological Services (CaPS)](https://www.cmu.edu/counseling/).
