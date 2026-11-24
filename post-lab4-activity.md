---
layout: default
title: "Post-Lab 4 Activity"
permalink: /post-lab4-activity/
---

# Post-Lab 4 Activity

In Lab 4 Part II, you described a modeling task(s) for your project, including desired inputs and outputs, evaluation criteria, and training setup. You either tested an off-the-shelf model on it or described a detailed plan and identified potential bottlenecks. Today, you will consider what a reinforcement learning (RL) "environment" for your task (or one of them, if you specified multiple) might look like.

We encourage you to work with other members of your project group, and you are welcome to discuss answers with people outside of your project group-- for questions marked [GROUP], you may optionally submit the same answer as people you worked with. This is a "normal" Reflection assignment, so polished prose is not required! Other than the parts of the assignment where we ask you to copy and paste an LLM output directly, please write responses on your own or with your group without AI assistance. (Speech-to-text is still allowed as usual)


## What to do

Submit your answers by Tuesday, December 1 at 11:59pm ET (Reflection 6). 3-5 sentences per question for Q2-6 is plenty!

1. Pick one task from your Lab 4 Question 8 and describe it below (You may copy-paste parts of your answer!) If you have not yet completed this part of the lab, consider working on this Reflection with a classmate from another group
2. **What is an "RL environment"?** People currently use this term in several different ways. There is a "classical" definition and also a looser working definition(s) used today in AI land. Look up two or three descriptions or examples (e.g. a textbook definition, a library, a company's product, a blog post, a paper) and (1) name them. (2) Describe one way they disagree or one thing they leave unclear (e.g. does a single prompt with a graded answer count? is an evaluation benchmark an environment?). (3) Is your task clearly a good or bad fit for learning in an "RL environment"? (Might task performance benefit from some "general" RL training to learn the domain? Do you think RL for your task could be a useful part of "general" RL training to learn a domain? Is RL overkill for your task?) Feel free to be brief on the third question; you will answer more in depth in Q6
3. **Sketch an RL environment.** [GROUP] Describe an environment for your task under this definition: (1) a set of tasks or starting situations, (2) what the model can see and do while attempting one, and (3) a way of scoring the attempt automatically. Which of these was hardest to specify? 
4. **Break it.** [GROUP] Assume a model trained in your environment will get better at earning the reward that you specify (in practice, this part also often takes work to get right!). (1) Describe at least one way to get a high score *without* doing the task well. (If you are working with or near someone, trade sketches and try to break each other's!) (2) Sketch a rough v2 of your environment in response, **and/or** describe why it's hard to improve "intended" learning in practice for your task
5. **Ask an LLM.** Now prompt an LLM of your choice to design an RL environment for the same task. Name the model, and paste your prompt and its output. Discuss in 3-5 sentences. Guiding questions (no need to answer every single one completely): How does its environment differ from yours? Anything you think is a good idea? Bad idea? Anything it suggests that might be based on a misunderstanding of your task? Anything that would be infeasible in practice for an academic?
6. **Step back.** Do you actually *like* the idea of an "RL environment" for a project task? (Feel free to refer back to and/or flesh out your response to Q2) Other guiding questions: Do you prefer the way you set it up in your Lab 4 Part II? (/Is it basically the same??) Is your environment anything more than an evaluation set with a score? How does its score compare with the "first check" you described in Lab 4 Question 9? Would you actually want a model trained this way for your project?
7. **Collaboration statement.** [GROUP] Did you work with anyone? If so, state their name(s) and Andrew ID, and briefly describe how you worked together.


If you missed class, you may complete this Reflection on your own time (reminder that your lowest Reflection submission will be dropped!)
