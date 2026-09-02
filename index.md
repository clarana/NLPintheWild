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
  - [Schedule](#schedule)
  - [Assignments](#assignments)
    - [Labs and project](#labs-and-project)
    - [Reflections](#reflections)
  - [Policies](#policies)
  - [FAQ (ongoing)](#faq-ongoing)






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

**Group A**: You are a student in a discipline outside of ML/NLP (e.g. a sufficiently different discipline within computing such as programming languages, or an entirely separate discipline such as English, biology or design), and you are interested in using language technologies (e.g. machine learning with text data, LLMs) for your work. You do not need to have a specific use case yet– part of the course's objective will be to refine a research question in the context of available resources and technology. However, you should have an understanding in general of what it looks like to do research in your discipline

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
| **Canvas** | [canvas.cmu.edu/courses/56179](https://canvas.cmu.edu/courses/56179) |
| **Piazza** | [piazza.com/class/mshlvaz248d7f5](https://piazza.com/class/mshlvaz248d7f5/) |
| **Contact** | Please use Piazza for questions. For private matters, make a private post on Piazza and/or email the instructors. |

## Topics

In this course, students will do natural language processing "in the wild" to conduct research in a specialized domain: they will build a text-based dataset, measure and make claims about their data, and adapt language technologies to their dataset.

<details class="topic" id="part-1-text-as-data-and-language-technologies" markdown="1">
<summary>Part 1: Text as data and language technologies</summary>

Students will begin by exploring general techniques and tools for analyzing text as data. Students will consider a historical perspective of natural language processing, learning about assumptions and tools for language processing that have evolved throughout the years, as well as underlying paradigms and constraints that have persisted even as our methods and surroundings have shifted.

Students will implement and compare various ways to encode language and text as information that one can study with a computer; by the end of the unit, students will be familiar with common use cases and limitations of methods for exploratory text data analysis, spanning command line tools, programming language-native functions, off-the-shelf libraries for natural language processing, and custom implementations. In particular, students will gain an understanding of differences in common methods and assumptions' relevance across different settings; certain differences in domain or motivation may simply call for adjusted hyperparameters, while others may warrant entirely different toolsets or additional processing of text.

Examples of concepts and tools students will encounter:
- How to represent and model language, and at what level?
  - Bytes, subwords, words, sequences, documents, and corpora
  - Syntax, semantics, and discourse
  - Vectorized representations of language such as bag-of-words representations (unweighted, weighted), static word embeddings (e.g. GloVe), contextual word embeddings (e.g. BERT)
  - Graph representations of language such as dependency parses and HTML
- Processing language given a representation
  - Finding and/or transforming text using regular expressions, string functions, fuzzy matching, and Unix commands such as jq, sed, and grep
  - Tagging language with predetermined labels (e.g. named entity recognition or sequence classification), or describing language in relative terms (e.g. LDA topic models)


</details>

<details class="topic" id="part-2-navigating-tools-and-affordances" markdown="1">
<summary>Part 2: Navigating tools and affordances</summary>

In the second section, students will build their own corpus. Throughout, students will repeatedly confront the challenge of determining 1) what work needs to be done, 2) what tools already exist for performing this work, and 3) how well-suited existing tools are. In general, students will practice thinking about data, algorithms, metrics, settings, models, software, and hardware as affordances they may consider for off-the-shelf use to achieve some or even most aspects of their goals. 

Examples of concepts and tools students will engage with:
- Data storage and navigation (e.g. search engines, ElasticSearch, BM25, RAG embeddings)
- The World Wide Web and Internet (e.g. APIs, web scraping, network protocols)
- Large language models, MCPs, and agents
- Data governance (e.g. licenses, filters, provenance, privacy)

</details>

<details class="topic" id="part-3-data-curation-and-evaluation" markdown="1">
<summary>Part 3: Data curation and evaluation</summary>

In the next section, students will choose appropriate evaluation protocols, assess the quality and suitability of evaluation protocols themselves, and both specify and perform data annotation labor as they consider ways to answer their specific research questions.

Examples of concepts and tools students will engage with:
- Annotation tasks and labor
- Measures of annotator agreement
- Benchmarks, metrics, and metric validity and reliability
- Quantitative and qualitative analysis
- "In domain" vs out-of-distribution data

</details>

<details class="topic" id="part-4-adapting-models-to-domains" markdown="1">
<summary>Part 4: Adapting models to domains</summary>

In the final section of the course, students will consider and try various methods for adapting existing models to their use cases, with a deep focus on LLMs. Methods discussed will span light-weight context augmentation (e.g. in-context learning), resource-intensive pre-training from scratch, and many techniques in-between. Notably, techniques do not fall along a universal one-dimensional scale in either cost or complexity. 

Examples of concepts and tools students will engage with:
- In-context adaptation (e.g. few-shot learning, system prompts, agent skills, retrieval augmented generation)
- Parametric adaptation (e.g. supervised fine-tuning, "mid-training", reinforcement learning, offline or online model merging)
- Synthetic data generation 
- Lifelong / continual learning

</details>

## Schedule

Dates are tentative and subject to change. In-class exercise materials, assignment links, and readings will be posted here as the semester progresses. Unless stated otherwise, all assignments are due at **11:59pm Eastern (ET)** on the listed date.

<!-- The color rail on the left marks which course Part each class belongs to: -->
<div class="unit-legend" markdown="0">
  <a class="unit-chip u1" href="#part-1-text-as-data-and-language-technologies">Part 1 · Text as data</a>
  <a class="unit-chip u2" href="#part-2-navigating-tools-and-affordances">Part 2 · Tools and affordances</a>
  <a class="unit-chip u3" href="#part-3-data-curation-and-evaluation">Part 3 · Data curation and evaluation</a>
  <a class="unit-chip u4" href="#part-4-adapting-models-to-domains">Part 4 · Adapting models</a>
</div>

<div class="table-scroll" markdown="0">
<table class="schedule">
  <thead>
    <tr>
      <th>Wk</th>
      <th>Date</th>
      <th>Lecture</th>
      <th>In-class activity</th>
      <th>Assignments</th>
      <th>Readings &amp; resources</th>
    </tr>
  </thead>
  <tbody>
  {% assign prev_week = "" %}
  {% for s in site.data.schedule %}
    {% assign row_class = "" %}
    {% if s.unit %}{% assign row_class = row_class | append: " u" | append: s.unit %}{% endif %}
    {% if s.week and s.week != prev_week %}{% assign row_class = row_class | append: " week-start" %}{% endif %}
    {% if s.no_class %}{% assign row_class = row_class | append: " no-class" %}{% endif %}
    <tr{% if row_class != "" %} class="{{ row_class | strip }}"{% endif %}>
      <td>{% if s.week and s.week != prev_week %}{{ s.week }}{% endif %}</td>
      <td>{% if s.date %}{{ s.date | date: "%a %b %-d" }}{% elsif s.date_label %}{{ s.date_label }}{% else %}TBD{% endif %}</td>
      <td>{% if s.no_class %}<em>{{ s.lecture }}</em>{% else %}{% if s.lecture_no %}<span class="lec-no">L{{ s.lecture_no }}</span> {% endif %}{% if s.slides %}<a href="{{ s.slides | relative_url }}">{{ s.lecture }}</a>{% else %}{{ s.lecture }}{% endif %}{% if s.speaker %} &middot; {% if s.speaker.url %}<a href="{{ s.speaker.url }}">{{ s.speaker.name }}</a>{% else %}{{ s.speaker.name }}{% endif %}{% endif %}{% endif %}</td>
      <td>{% for a in s.activity %}{{ a | markdownify | remove: '<p>' | remove: '</p>' | strip }}{% unless forloop.last %}<br>{% endunless %}{% endfor %}</td>
      <td>{% for a in s.assignments %}{% if a.text %}{% if a.tag %}<span class="atag atag-{{ a.tag }}">{{ a.tag }}</span> {% endif %}{{ a.text | markdownify | remove: '<p>' | remove: '</p>' | strip }}{% else %}{{ a | markdownify | remove: '<p>' | remove: '</p>' | strip }}{% endif %}{% unless forloop.last %}<br>{% endunless %}{% endfor %}</td>
      {%- comment -%} Readings live on their own page per class meeting: _readings/<class date>.md, matched on class_date. An inline `readings:` list in schedule.yml still renders, as a one-off override. {%- endcomment -%}
      {%- assign rkey = s.date | date: "%Y-%m-%d" -%}
      {%- assign rdoc = site.readings | where: "class_date", rkey | first -%}
      <td>{% if rdoc %}<a href="{{ rdoc.url | relative_url }}">{% if s.class_no %}Day {{ s.class_no }} readings{% else %}Readings &amp; resources{% endif %}</a>{% endif %}{% if rdoc and s.readings %}<br>{% endif %}{% for a in s.readings %}{{ a | markdownify | remove: '<p>' | remove: '</p>' | strip }}{% unless forloop.last %}<br>{% endunless %}{% endfor %}</td>
    </tr>
    {% if s.week %}{% assign prev_week = s.week %}{% endif %}
  {% endfor %}
  </tbody>
</table>
</div>

## Assignments

Grades are based on a combination of individual and group work.

| Component | Weight |
|---|---|
| Reflections | 20 |
| Introductory Presentations | 8 |
| Labs | 36 |
| Project | 36 |

**Reflections (20 points).** (6 assignments; 4 points each. Lowest grade dropped. Individual.) Reflections are meant to encourage engagement in and reflection on class lectures, especially with respect to goals and interests the student originally entered the class with. Specific prompts and questions will vary from reflection to reflection. More details below and in class.

**Introductory Presentations (8 points).** (1 assignment. Individual.) Students introduce themselves, their research interests, and their goals for the class, with a focus on communicating their research area's norms and practices to be legible to their classmates and a braoder academic audience. More details forthcoming.
<!-- NLP students sign up to present on their own work and/or an adaptation method they are familiar with, and non-NLP students sign up to present on their own work and/or a dataset they are hoping to work with. All students identify goal(s) they are hoping to accomplish in taking the course. These introductory presentations will help students form teams for later labs and the course project. -->

**Labs (36 points).** (4 assignments; 9 points each. First lab is individual, the rest are group.) Labs are implementation- and analysis-heavy assignments (mostly Python/PyTorch) designed to give hands-on experience implementing the methodologies discussed in class. After the first lab, labs will be group assignments to be completed with project teams using the codebase being developed for your course project. All labs will have "tracks" or components for NLP students and non-NLP students.

**Project (36 points).** (Group.) A semester-long 2-4 person team project focused on carrying out a research goal within a particular domain of interest to people in a non-NLP discipline. There will be intermediate assignments and exercises (project proposal, project sharing, writing abstracts for each other's publication audiences) as well as a final presentation and report. More details below and in class.

### Labs and project
{% assign labs = site.labs | sort: "nav_order" %}
{% for lab in labs %}
<div class="assignment-summary">
  <h4 style="margin-bottom:.2em"><a href="{{ lab.url | relative_url }}">{{ lab.title }}</a> <small>&ndash; {% if lab.due %}due {{ lab.due | date: "%b %-d, %Y" }}, 11:59pm ET{% else %}due TBD{% endif %}{% if lab.points %}, {{ lab.points }} pts{% endif %}</small></h4>
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

**Late Work:** Unless stated otherwise, assignments are due at 11:59pm Eastern (ET) on the date listed in the schedule. Every student begins the semester with 5 late days to use across individual assignments over the semester, and every project group receives a separate 5 late days to use across group assignments. One late day extends a deadline by 24 hours, and late days are used in whole-day increments. Late work beyond late days will be accepted only in extenuating circumstances. Late days will be applied automatically (no need to ask ahead of time or state a specific reason!) and are meant to cover most situations that would warrant an extension, including but not limited to conference travel, minor illness, competing deadlines, and (minor) personal emergencies. For extenuating circumstances beyond what standard late days can cover, contact the instructors.

**Academic Integrity:** Throughout the semester, students will be asked to complete work individually, in groups, and using various types and amounts of technology, e.g. generative AI. Different components of the same assignment may vary in expectation; expectations and learning objectives will be explicitly communicated to students. In general, students are asked to uphold the spirit of each assignment. When in doubt, ask the instructors

**Accommodations:** If you have a disability and require accommodations but do not already have them approved by the Office of Disability Resources, please apply for accommodations through the Application section of the [Disability Resources Online Portal](https://rainier.accessiblelearning.com/cmu/start). If you already have accommodations approved with Disability Resources, please use the [Accommodations Management](https://rainier.accessiblelearning.com/cmu) section of the Disability Resources Online Portal to notify me about your accommodations, and discuss your accommodations and needs with the instructors as early in the semester as possible. We will work with you to ensure that accommodations are provided as appropriate.

**Wellness:** As a student, you may experience a range of challenges that can interfere with learning, such as strained relationships, increased anxiety, substance use, feeling down, difficulty concentrating and/or lack of motivation. This is normal, and all of us benefit from support during times of struggle. There are many helpful resources available on campus and an important part of a healthy life is learning how to ask for help. Asking for support sooner rather than later is almost always helpful. CMU services are available free to students, and treatment does work. You can learn more about confidential mental health services available on campus through [Counseling and Psychological Services (CaPS)](https://www.cmu.edu/counseling/). Support is always available (24/7) at: 412-268-2922.

## FAQ (ongoing)

<details class="faq" markdown="1">
<summary>Do I need my own dataset or research question already?</summary>

No, but you are more than welcome to join the class with a specific dataset or research question in mind already! All students will be asked to refine a research question in the context of the resources and technology available to them, and to acquire or develop resources in service of their project.
</details>


<details class="faq" markdown="1">
<summary>Do expectations for Group A and Group B students differ?</summary>

All students will be expected to complete all assignments. Already having experience with a particular topic or tool (e.g. setting up an annotation study, or training a model) may put a student in a position to assist other students with some in-class exercises. However, in general, the course and its assignments are designed to emphasize reflection, collaboration, and critical engagement with tools and their limitations. By design, assignments will be non-trivial to complete regardless of previous experience-- in fact, students will often be provided implementations of tools to use in assignments, and in many cases a majority of the work expected of students will be reflective and interpretative. 

Course projects will be assessed on a case-by-case basis, in collaboration with students. Expectations will be calibrated to a variety of factors, where depth of previous NLP experience will be just one of multiple factors, alongside considerations such as ambition of project goals, availability of existing tools and resources, and difficulty of acquiring or developing additional relevant tools and resources. 
</details>
