import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells

    import marimo as mo

    import random
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
    ASSIGNMENT = "Assignment 1, Part I"  # assignment name, or a one-line purpose
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

    In the first part of of Assignment 1, you will:
    * Set up a local `uv` environment
    * Load the 20 Newsgroups corpus and explore it
    * Train and tune topic models on the documents from the corpus

    Please follow this notebook for demonstrations and scaffolding interleaved with questions for you to answer.

    **When you are finished, you will submit this marimo notebook, filled out with your answers, along with the auto-saved `model_history.csv` record of models you trained (more below)**

    All questions will be marked as a numbered Question under an h3 heading, like ``### Question 0:'' with a cell immediately below for you to type your answers.

    The code blocks immediately below are a Q&A registry-- as you write answers throughout the notebook, your answers will populate up here!
    """)
    return


@app.cell
def _():
    QUESTIONS = {
        1: "First model's first impressions",
        2: "Preprocessing 1", # via LDA class,
        3: "Random seed variation",
        4: "Varying k",
        5: "Varying alpha and eta",
        6: "How much to train?",
        7: "Preprocessing 2", # via pre-vectorization
        8: "Discussing labels and metrics",
        9: "Goal-directed exploration"
    }
    PLACEHOLDER = "(write your answer here)"
    return PLACEHOLDER, QUESTIONS


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
    ANSWERS = {1: answer_1, 2: answer_2, 3: answer_3, 4: answer_4, 5: answer_5, 6: answer_6, 7: answer_7, 8: answer_8, 9: answer_9} # blank answer variables are defined throughout!
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
    # Loading data

    For this first part of Assignment 1, we will work with an established dataset. The [20 Newsgroups](http://qwone.com/~jason/20Newsgroups/) corpus is so prevalent that it is available directly through `scikit-learn` as a canonical "example" dataset. For today, we will load the dataset via the [Hugging Face Hub](https://huggingface.co/docs/hub/datasets-downloading), a common ecosystem hosting models, datasets, and software affordances associated with AI models, especially language models and text datasets.
    """)
    return


@app.cell
def _():
    newsgroups_train = load_dataset("SetFit/20_newsgroups", split="train")
    newsgroups_train
    # 11,314 docs; columns: text, label, label_text
    return (newsgroups_train,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This is probably the simplest kind of data load you will do for this class!

    Both Hugging Face `datasets` and native `sklearn` datasets allow you to skip many of the preprocessing steps described [here](http://qwone.com/~jason/20Newsgroups/)


    Use the block below to explore, but feel free to comment it out in your final submission!
    """)
    return


@app.cell
def _():
    # # Extra info: the same dataset loaded in with sklearn comes with its own object structure. 
    # # from sklearn.datasets import fetch_20newsgroups # import directly from sklearn

    # # newsgroups_train_sk = fetch_20newsgroups(subset="train") # load directly

    # # print(newsgroups_train_sk.target_names) # inspect list of 20 news group names
    # _i=2

    # print("Text of third article: \n", newsgroups_train["text"][_i], end="\n=====\n") # This is relevant to running `print(newsgroups_train_sk.data[_i])`")

    # print(newsgroups_train["label"][_i], "is the news group index of the same third article") # equivalent to `print(newsgroups_train_sk.target[_i])`

    # print(newsgroups_train["label_text"][_i], "is the news group name of the same third article") # equivalent to `print(newsgroups_train.target_names[_i])`
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Preprocessing Text

    In this section, we'll go through how we might transform a string into a vectorized representation, suitable for being used in a topic model.

    ## Tokenization

    _Tokenization_ refers to the process of splitting blocks of text up into the units that you want to be counting. As we covered in lecture, this can be words or characters, and additionally might include n-grams. We'll cover some alternative approaches in next week's lecture.

    For languages like English, where space separation is not an unreasonable proxy, splitting based on whitespace isn't a terrible strategy. The `space_split` function below does exactly this.

    But in text that we find, there might be other kinds of whitespace: newlines, tabs, etc. Additionally, we might want to do things like tokenize possessives as two tokens, instead of one: e.g. "Andrew's" might become `[Andrew, 's]` instead of `[Andrew's]`. Similarly, we might not want terminal punctuation to be part of tokens.

    ## Normalization

    _Normalization_ here refers to choices that you make that might disregard some information about a piece of text, in order to represent it in a standardized way. A great example here is case: do you want to treat a word with an initial capital different than the same word that's all lowercase? What about words that are all uppercase?

    Stopword removal is also arguably a kind of text normalization: you're removing words that you argue are vestigial.

    ## The library approach

    In the cell below, we'll demonstrate how to use the Scikit-learn CountVectorizer to achieve some of the goals we've talked about here. We've passed the parameters that relate to each of the things we discussed above explicitly; take a look at the class's [documentation](https://scikit-learn.org/0.15/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) to learn more about more of the parameters.

    With a library like scikit-learn, **remember to always check the default options when you are using a class** like CountVectorizer. These libraries can be opinionated, and it might lead to unintended consequences!
    """)
    return


@app.cell
def _():
    # scikit-learn requires that we instantiate a class before using it. 
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
    return (vectorizer,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    After we define our CountVectorizer, we can "fit" it to the corpus that we have - it will automatically keep track of e.g. what tokens occur, so that we have a vocabulary, and will additionally allow us to generate the vectorized version of our corpus. We can combine these two functions with the `fit_transform` method, or run `fit` and `transform` independently.
    """)
    return


@app.cell
def _(newsgroups_train, vectorizer):
    vectorized_corpus = vectorizer.fit_transform(newsgroups_train['text'])
    vectorized_corpus.shape
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    After we've run our vectorizer over the corpus, we can see that we've got a matrix, with a number of rows that corresponds to the number of documents, and a number of rows that corresponds to the vocabulary size. Try changing the parameters to see how it affects the vocabulary size!

    To transform a new document, you can run the `transform` method with the fitted vectorizer. Note that the `transform` method takes a list of documents! The method returns a **sparse** vector, so that the many 0 values do not take up space.
    """)
    return


@app.cell
def _(newsgroups_train, vectorizer):
    vectorizer.transform([newsgroups_train['text'][0]])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Additionally, we can get a tokenizer function, or a combined preprocess-and-tokenize function by calling `build_tokenizer` and `build_analyzer`, respectively:
    """)
    return


@app.cell
def _(vectorizer):
    tokenizer = vectorizer.build_tokenizer()
    tokenizer("This is test text! Look what happens to this text")
    return


@app.cell
def _(vectorizer):
    analyzer = vectorizer.build_analyzer() # for now, it does the same thing, because our preprocessing is minimal!
    analyzer("This is test text! Look what happens to this text")
    return (analyzer,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Running a topic model

    Here, we'll build a topic model that depends on our vectorizer and the text that it produces. In keeping with [Maria Antoniak's blog post](https://maria-antoniak.github.io/2022/07/27/topic-modeling-for-the-people.html), we'll be using a library called [Tomotopy](https://bab2min.github.io/tomotopy/), which implements Gibbs sampling, rather than variational inference.

    We start very similarly to scikit-learn: defining a "model" object that we later fit. Here, Tomotopy also expects us to "add documents" to the model. Documents added in this way will be used to fit the model.

    Take a look at the documentation to understand some of these parameters better. We'll be asking you to vary them systematically for this assignment. However, for this first run, use these hardcoded values:
    """)
    return


@app.cell
def _():
    basic_topic_model = LDAModel(
        min_cf=0,
        min_df=0,
        rm_top=0,
        k=20,
        alpha=0.1,
        eta=0.01,
        seed=42,
    )
    return (basic_topic_model,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Tomotopy expects its "documents" as lists of tokens. Here, we can use the analyzer we've already built with scikit-learn:
    """)
    return


@app.cell
def _(analyzer, basic_topic_model, newsgroups_train):
    kept_indices = []   # kept_indices[j] = original newsgroups_train row for model doc idx j
    for _i, _text in enumerate(newsgroups_train['text']):
        if basic_topic_model.add_doc(analyzer(_text)) is not None:
            kept_indices.append(_i)

    len(basic_topic_model.docs)  # notice that we end up with fewer docs than we started with!
    return (kept_indices,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Training the topic model

    We can "train" our topic model (i.e. associate documents to topics, and topics to words), by running the following cell. Note how perplexity (how well the model "predicts" the text) decreases as we train this model:
    """)
    return


@app.cell
def _(basic_topic_model):
    for i in range(0, int(1000), int(100)):
        basic_topic_model.train(int(100))
        print('Iteration: {}\tLog-likelihood: {}\tPerplexity: {}'.format(i, basic_topic_model.ll_per_word, basic_topic_model.perplexity))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Examining the topic model

    Once we have trained our model, we can examine the topics by their top words: this is typically how people will "label" their topics.

    Tomotopy also provides a handy `summary()` method, that will give you an overview of what your topic model is doing.

    If in VSCode, you may have to click "view as a scrollable element" or use another workaround to see truncated output!
    """)
    return


@app.cell
def _(basic_topic_model):
    # for k in range(basic_topic_model.k):
    #     print('Top 10 words of topic #{}'.format(k))
    #     print(basic_topic_model.get_topic_words(k, top_n=10)) # more manual way of getting topic model info

    basic_topic_model.summary(topic_word_top_n=50)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 1: Initial impressions

    **Now that you have trained your first topic model (with k=10 topics, 1000 steps, and default hyperparameters), state your initial impressions of the generated topics.** List just 2 impressions, in ~2 sentences.

    Some ideas and examples to get you started: "about X% of these topics make no sense" or "i was surprised there was not a topic on \_\_\_\_\_" or "I didn't anticipate XYZ being a topic but it makes sense given ABC thing about how the algorithm works"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_1 = rf"""
    {PLACEHOLDER}
    """
    return (answer_1,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Vocabulary frequency thresholds

    Look at the `summary()` output above. Most topics share the same handful of top words: "the", "to", "of", "and", "I". With an unfiltered vocabulary, the most frequent tokens end up in every topic, and the long tail of the vocabulary is full of tokens that appear once (typos, email addresses, and blocks of gibberish like `AX`, `MAX`, `Q`, which are likely artifacts of files pasted into posts as text) and say nothing about topics.

    Tomotopy's `LDAModel` takes three arguments that prune the vocabulary before training starts:

    * `min_cf`: drop tokens whose total count across the whole corpus (its _collection frequency_) is below this number.
    * `min_df`: drop any token that appears in fewer than this many documents (its _document frequency_).
    * `rm_top`: after the two filters above, drop the N most frequent tokens that remain.

    These are arguments passed in as the `LDAModel` object is being initialized. A model cannot be "reset" with new thresholds. Each new set of thresholds means a new model object, then `add_doc` and `train` again. Pruned tokens stay inside the documents but are ignored during training; the number of documents does not change, and our `kept_indices` from above still maps model documents back to `newsgroups_train` for any model trained on the same token lists. A document whose every token was pruned stays in the model with no words; its topic distribution is then just the prior.

    The table below lists every distinct token that `basic_topic_model` saw, with its collection frequency and document frequency, most frequent first. Find `AX` in it: it is the second most frequent token in the whole corpus (62,384 occurrences), but it shows up in only 17 documents. Which of the three arguments would remove it, and which would not? (No need to write the answer down; it is a warm-up for Question 2.) The two small tables after it apply one argument at a time. `min_df` and `min_cf` cut the tail of the list: the count of surviving tokens drops fast, but the head of the list barely moves. `rm_top` cuts the head: each column shows the most frequent tokens left after it.
    """)
    return


@app.cell
def _(basic_topic_model):
    # every distinct token basic_topic_model saw, most frequent first. Sort or search the table (try "AX").
    vocab_table = pd.DataFrame({
        "token": list(basic_topic_model.vocabs),
        "collection frequency": list(basic_topic_model.vocab_freq),  # what min_cf looks at
        "document frequency": list(basic_topic_model.vocab_df),      # what min_df looks at
    }).sort_values("collection frequency", ascending=False, ignore_index=True)
    mo.ui.table(vocab_table, selection=None, page_size=10)
    return (vocab_table,)


@app.cell
def _(vocab_table):
    # what min_df and min_cf do to the list above, one argument at a time (the other two stay 0).
    # Both cut the tail. The last column lists the 5 most frequent tokens that min_df = d drops;
    _thresholds = (2, 5, 10, 20, 50, 100)
    _sorted_vocab = vocab_table["token"]
    pd.DataFrame(
        {
            f"tokens kept if min_df = _t (of {len(vocab_table):,})": [int((vocab_table["document frequency"] >= _t).sum()) for _t in _thresholds],
            f"tokens kept if min_cf = _t (of {len(vocab_table):,})": [int((vocab_table["collection frequency"] >= _t).sum()) for _t in _thresholds],
            "5 most frequent tokens dropped by min_df=_t": [(f"" + ", ").join(vocab_table.loc[vocab_table["document frequency"] < _t, "token"].head(5)) for _t in _thresholds],
        },
        index=pd.Index(_thresholds, name="_t"),
    )
    return


@app.cell
def _(vocab_table):
    # rm_top cuts the head: each column holds the 10 most frequent tokens the model would still train on after rm_top removes that many.
    # (fixing min_df = min_cf = 0)
    pd.DataFrame(
        {f"rm_top={_n}": vocab_table["token"].iloc[_n:_n + 10].to_numpy() for _n in (0, 10, 20, 50, 100, 200)},
        index=pd.RangeIndex(1, 11, name="rank"),
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    From here on we'll train a lot of models, so two shortcuts first. `show_topics` prints one row per topic: the share of the model's kept tokens assigned to it (pruned tokens are not counted), how many of its top words are on scikit-learn's English stop-word list, then the top words. That is easier to compare across models than the full `summary()`:
    """)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    And we tokenize the corpus once, so that most models from here on can train on exactly the same token lists:
    """)
    return


@app.cell
def _(analyzer, newsgroups_train):
    # tokenize once, reuse for later models
    tokenized_docs = [analyzer(_text) for _text in newsgroups_train["text"]]
    tokenized_docs = [_doc for _doc in tokenized_docs if _doc]  # skips the same empty docs that add_doc() skipped above, so kept_indices still applies
    len(tokenized_docs)
    return (tokenized_docs,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Training a Second Model

    One common  `min_df`: drop tokens that appear in fewer than a few documents. Here is a second model, identical to `basic_topic_model` except for `min_df=20`.

    **NOTE:** From here on the notebook trains several models when it opens, roughly 15 to 45 seconds each at 1000 steps, depending on your machine. Editing a cell above them, such as the `CountVectorizer` cell, retrains everything below it.
    """)
    return


@app.cell
def _(tokenized_docs):
    topic_model_v2 = LDAModel(
        min_cf=0,
        min_df=20,     # the only change from basic_topic_model
        rm_top=0,
        k=20,
        alpha=0.1,
        eta=0.01,
        seed=42,
    )
    for _doc in tokenized_docs:
        topic_model_v2.add_doc(_doc)
    for _i in range(0, 1000, 100):
        topic_model_v2.train(100)
    print(
        f"kept {len(topic_model_v2.used_vocabs):,} of {len(topic_model_v2.vocabs):,} distinct tokens; "
        f"removed as top words: {list(topic_model_v2.removed_top_words)}\n"
        f"log-likelihood/word: {topic_model_v2.ll_per_word:.3f}   perplexity: {topic_model_v2.perplexity:.1f}"
    )
    return (topic_model_v2,)


@app.cell
def _(basic_topic_model, show_topics, topic_model_v2):
    mo.ui.tabs({
        "basic_topic_model": show_topics(basic_topic_model, top_n=15),
        "topic_model_v2": show_topics(topic_model_v2, top_n=15),
    })
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Observe that only a small proportion of the original distinct tokens are gone, and perplexity dropped noticeably.

    Keep in mind, however, that perplexity is just exp(-log-likelihood per word), and a smaller vocabulary makes every remaining word easier to predict, so neither number is comparable between models that kept different tokens. Perplexity and log likelihood values are only safe to compare between runs with the same `min_cf`, `min_df`, and `rm_top`.

    Now look at the top words and the stop-word column. You might feel that the topics are noticeably different, but also that there are still lots of uninformative topics. Dropping rare tokens does nothing about frequent ones; in Question 2 you will be asked to try out one more reasonable setting and report your observations
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 2: Vocabulary frequency thresholds

    **Propose one combination of `min_cf`, `min_df`, and `rm_top` that you think will improve the topics, and try it as `topic_model_v3` in the cell below.** Did it help? Answer in ~3 sentences: which values you chose and why? What changed in the topics relative to `basic_topic_model` and `topic_model_v2`?


    Note that, the hyperparameters for `topic_model_v3` are initially set to be identical to the ones we had for `basic_topic_model`.

    Some ideas and examples to get you started: "I set rm_top=N because the N most frequent tokens were all \_\_\_\_\_" or "`min_df`=X got rid of the gibberish like AX, but the topic about \_\_\_\_\_ disappeared too" or "it helped for about half the topics, but the topics made of digits are still there". One attempt with a before/after comparison is enough! No need to find the "best" settings :)
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_2 = rf"""
    {PLACEHOLDER}
    """
    return (answer_2,)


@app.cell
def _(tokenized_docs):
    # Question 2 skeleton
    # TODO: change the three threshold arguments, then re-run this cell
    topic_model_v3 = LDAModel(
        min_cf=0,    # <- your value
        min_df=0,    # <- your value
        rm_top=0,    # <- your value
        k=20,        # keep k, alpha, eta, and seed fixed so that the thresholds are the only change
        alpha=0.1,
        eta=0.01,
        seed=42,
    )
    for _doc in tokenized_docs:
        topic_model_v3.add_doc(_doc)
    for _i in range(0, 1000, 100):
        topic_model_v3.train(100)
    print(
        f"kept {len(topic_model_v3.used_vocabs):,} of {len(topic_model_v3.vocabs):,} distinct tokens; "
        f"removed as top words: {list(topic_model_v3.removed_top_words)}\n"
        f"log-likelihood/word: {topic_model_v3.ll_per_word:.3f}   perplexity: {topic_model_v3.perplexity:.1f}"
    )
    return (topic_model_v3,)


@app.cell
def _(basic_topic_model, show_topics, topic_model_v2, topic_model_v3):
    mo.ui.tabs({
        "basic_topic_model": show_topics(basic_topic_model),
        "topic_model_v2 (min_df=20)": show_topics(topic_model_v2),
        "topic_model_v3 (yours)": show_topics(topic_model_v3),
    })
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Marimo UI objects to help you iterate

    Before we have you start training many more topic models, run these cells-- you will not use all of these values right away, but you will end up finding them helpful as you vary the number of topics, number of training iterations, random seed, and alpha and eta parameters.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Viewing document topics

    Additional exploratory tool: You can view which documents are associated with which topics by accessing the documents in the model with the `docs` function, and then calling `get_topic_dist` on an individual doc:
    """)
    return


@app.cell
def _(
    basic_topic_model,
    model_history,
    topic_model,
    topic_model_v2,
    topic_model_v3,
):
    # Example: Choose which model the document viewer below looks at.
    # This cell reads `topic_model`, so it refreshes after every run of the training form further down.
    # topic_model_v4 (Question 7) is left out on purpose: it is trained on different token lists, so the viewer
    # would need kept_indices_v2 instead of kept_indices to map its documents back to newsgroups_train.
    _options = {
        "basic_topic_model": basic_topic_model,
        "topic_model_v2": topic_model_v2,
        "topic_model_v3": topic_model_v3,
    }
    _options.update({_label: _run["model"] for _label, _run in model_history.items()})
    _default = "basic_topic_model"
    if topic_model is not None:   # follow the active form run (form settings + active seed)
        _default = next(_l for _l, _m in _options.items() if _m is topic_model)
    model_picker = mo.ui.dropdown(options=_options, value=_default, label="Model to inspect")
    model_picker
    return (model_picker,)


@app.cell
def _(basic_topic_model):
    i_doc = mo.ui.slider(start=0, stop=len(basic_topic_model.docs)-1, show_value=True, label="Document index", include_input=True)
    i_doc
    return (i_doc,)


@app.cell
def _(i_doc, kept_indices, model_picker, newsgroups_train):
    _model_docs = list(model_picker.value.docs)
    # NOTE: tomotopy 0.14.0 flips out if you don't manually cast an LDA model's `docs` to a `list` before trying to index beyond 0
    _j = i_doc.value            # index into the model's docs
    _orig = kept_indices[_j]    # corresponding row in newsgroups_train
    _dist = _model_docs[_j].get_topic_dist() # topics dist in this one doc
    _top = sorted(range(len(_dist)), key=lambda _k: _dist[_k], reverse=True)[:5] # top 5 topics
    _row = newsgroups_train[_orig] # original newsgroup label
    mo.vstack([
        mo.md(
            f"**{model_picker.selected_key}: doc {_j}**  ->  **newsgroups_train[{_orig}]**"
            f" &nbsp; label: `{_row['label_text']}`\n\n"
            f"top topics (id: prob): "
            + ", ".join(f"{_k}: {_dist[_k]:.3f}" for _k in _top)
        ),
        mo.md(f"```\n{_row['text']}\n```"),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Predicting topics

    Topic models can also be deployed on "unseen" documents to predict the mixture of topics in them. This can be useful if you want to use a topic model as a classifier, based on the topics that it discovered. This may take a while!
    """)
    return


@app.cell
def _(analyzer, basic_topic_model):
    # Example: Create a document and infer its topics.
    _doc = basic_topic_model.make_doc(analyzer("I love writing about cars and driving"))
    topics = basic_topic_model.infer(_doc)
    return (topics,)


@app.cell
def _(basic_topic_model, topics):
    # Example: `infer` returns a (topic distribution, log-likelihood) pair; this shows the top of it.
    _dist, _ll = topics
    _top = sorted(range(len(_dist)), key=lambda _k: _dist[_k], reverse=True)[:3]
    mo.md(
        "`infer` returned a topic distribution and a log-likelihood. Top 3 topics for that sentence in `basic_topic_model`: "
        + "; ".join(
            f"**{_k}** ({_dist[_k]:.3f}: {', '.join(_w for _w, _p in basic_topic_model.get_topic_words(_k, top_n=5))})"
            for _k in _top
        )
        + f". Log-likelihood {_ll:.2f}."
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Try your own text below. To submit new text, type your text and use `cmd+enter` (or equivalent). The model is the one chosen in "Model to inspect" above, so you can also test the models you train later.

    Two things happen to your words before inference: 1) words the model never saw in training are dropped, and 2) words it pruned with `min_cf`, `min_df`, or `rm_top` get no topic. A short sentence may therefore rest on two or three tokens.
    """)
    return


@app.cell
def _():
    new_text = mo.ui.text_area(value="I love writing about cars and driving", label="Text to classify", rows=3, full_width=True)
    new_text
    return (new_text,)


@app.cell
def _(analyzer, model_picker, new_text):
    _tokens = analyzer(new_text.value)
    mo.stop(not _tokens, mo.callout(mo.md("Type at least one word above."), kind="warn"))
    _model = model_picker.value
    _doc = _model.make_doc(_tokens)                  # drops words the model never saw
    _dist, _ll = _model.infer(_doc, iterations=100)  # 100 sampling steps for this one document
    _used = [_model.vocabs[_w] for _w, _t in zip(_doc.words, _doc.topics) if _t != -1]   # -1 = pruned by the thresholds
    _top = sorted(range(len(_dist)), key=lambda _k: _dist[_k], reverse=True)[:5]
    _rows = ["| topic | prob | top words |", "|---|---|---|"] + [
        f"| {_k} | {_dist[_k]:.3f} | {', '.join(_w for _w, _p in _model.get_topic_words(_k, top_n=10))} |" for _k in _top
    ]
    mo.vstack([
        mo.md(
            f"**{model_picker.selected_key}** used {len(_used)} of {len(_tokens)} tokens: `{' '.join(_used) or '(none)'}`. "
            + ("" if len(_used) == len(_tokens) else "The rest are unknown to this model or pruned by its thresholds. ")
            + ("With no usable token, the distribution below is just the prior." if not _used else "")
        ),
        mo.md("\n".join(_rows)),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The controls below hold every setting for the rest of the assignment. The random seed comes first: "New random seed" adds a seed to a list, and the "Active seed" radio button picks which one to use. The form under it holds the three vocabulary thresholds, `k`, `alpha`, `eta`, and the number of training steps. Nothing trains until you press the form button, so you can move the sliders freely. Each trained model is stored in `model_history` together with the settings and the seed you used, and the active one is also available as `topic_model`. (`topic_model` always means the model for the current form settings and active seed; the numbered models `v2`, `v3`, and `v4` are the ones built by hand.)

    Once the form has been submitted, changing the active seed acts right away: a seed you already trained with switches `topic_model` to that run without retraining, and a new seed trains a new run with the current form settings.

    The `train_lda` function below does the same three steps you ran separately above: build the model, `add_doc` every document, `train`. One box in the form needs a word of explanation. By default tomotopy re-estimates `alpha` every 10 steps (`optim_interval=10`), so the `alpha` you set is only a starting value. `basic_topic_model` did this too: compare the per-topic `alpha` values in its `summary()` output above with the `0.1` you gave it. The "Fix alpha" box turns that off, so the `alpha` you set is the `alpha` the model uses. Leave it off unless a question asks for it (Question 5 does).

    If you edit the `CountVectorizer` cell near the top, every model below it retrains and the form resets. The runs already in `model_history` stay, so press the button again if you want a run on the new tokens.
    """)
    return


@app.cell
def _(tokenized_docs):
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
def _():
    model_history = {}

    from pathlib import Path
    HISTORY_CSV = (mo.notebook_dir() or Path.cwd()) / "model_history.csv"
    SESSION_STARTED = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    def history_row(label, run):
        """One row (a dict) for a model_history entry: its settings plus the numbers the table below shows."""
        model = run["model"]
        return {
            "run": label.split(":")[0],
            **run["settings"],
            "distinct tokens seen": len(model.vocabs),   # before thresholds; changes only if the CountVectorizer changed
            "tokens kept": len(model.used_vocabs),
            "log-likelihood/word": round(model.ll_per_word, 3),
            "perplexity": round(model.perplexity, 1),
        }

    return HISTORY_CSV, SESSION_STARTED, history_row, model_history


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Every model trained with the above ends up being saved in `model_history`

    We can manipulate the LDA sliders with some of marimo's UI controls:
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


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 3: Random seed variation

    **Train a model with the same settings, with three different seeds. What do you notice? Are there topics that come back every time? Are there useful topics that appear only once? What about junk topics that are common across seeds?**

    Answer in ~3 sentences. Recommended workflow: Keep every setting in the form below as their default values and press submit. Then run the couple cells below to display information about the topics generated. Then, once the form is submitted, each press of "New random seed" trains one more run with the current settings, and the "Active seed" radio switches `topic_model` (and the topic table, the document viewer, and the "active" column) between the runs you already have.

    After this question, feel free to just keep the last random seed active for the rest of your experiments.

    Some ideas and examples to get you started: "a \_\_\_\_\_ topic showed up in all three runs with almost the same top words" or "two runs had one topic about \_\_\_\_\_ and the third split it into \_\_\_\_\_ and \_\_\_\_\_" or "the number of topics that make no sense changed from run to run, so I'm not sure my Question 2 conclusion holds"

    Note: tomotopy prints a warning on every `train()` call: with a fixed seed, results can still differ a little when it trains on several threads. In practice we didn't notice a difference, so feel free to keep `workers=0` as a default
    Note: you will probably have to scroll down to see-- the model training / output. Feel free to move the Q3 cells around if that is helpful :)
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_3 = rf"""
    {PLACEHOLDER}
    """
    return (answer_3,)


@app.cell
def _(tokenized_docs, train_lda):
    # All other LDA settings except the seed in one form. Pressing the button will trigger another model training
    # This cell reads tokenized_docs and train_lda on purpose: if either changes (for example after an edit to the
    # CountVectorizer cell), the form is rebuilt with value None.
    _ = train_lda
    lda_form = mo.ui.dictionary({
        "k": mo.ui.slider(start=2, stop=60, step=1, value=20, show_value=True, include_input=True, label="Number of topics (k)"),
        "alpha": mo.ui.slider(steps=[0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0], value=0.1, show_value=True, label="alpha (document-topic prior)"),
        "eta": mo.ui.slider(steps=[0.001, 0.01, 0.05, 0.1, 0.5, 1.0], value=0.01, show_value=True, label="eta (topic-word prior)"),
        "fix_alpha": mo.ui.checkbox(value=False, label="Fix alpha at the slider value (Question 5). Off: tomotopy re-estimates alpha during training, as basic_topic_model did"),
        "iters": mo.ui.slider(start=100, stop=5000, step=100, value=1000, show_value=True, include_input=True, label="Training steps"),
        "min_cf": mo.ui.number(start=0, stop=100000, step=1, value=0, label="min_cf (drop tokens with total count below this)"),
        "min_df": mo.ui.number(start=0, stop=10000, step=1, value=0, label="min_df (drop tokens in fewer documents than this)"),
        "rm_top": mo.ui.number(start=0, stop=1000, step=1, value=0, label="rm_top (drop this many most frequent tokens)"),
    }).form(submit_button_label="Train a model with these settings", bordered=True)

    mo.vstack([lda_form, mo.md(f"_Each run trains on all {len(tokenized_docs):,} non-empty documents. Every run is kept in `model_history`. If you submit settings and a seed you already trained, the notebook switches to that run instead of training again._")])
    return (lda_form,)


@app.cell
def _(
    HISTORY_CSV,
    SESSION_STARTED,
    history_row,
    lda_form,
    model_history,
    seed_picker,
    train_lda,
):
    # Trains one model per (form settings, active seed) and files it in model_history.
    if lda_form.value is None:
        topic_model, ll_trace = None, []
        _out = mo.callout(mo.md("Nothing trained yet. Set the values above and press the button."), kind="info")
    elif any(_v is None for _v in lda_form.value.values()):
        # a number field that was cleared with the keyboard arrives as None; tomotopy rejects None for
        # min_cf / min_df / rm_top and silently runs unseeded for seed=None
        topic_model, ll_trace = None, []
        _out = mo.callout(mo.md("Every field in the form needs a number. Fill in the empty one and press the button again."), kind="warn")
    else:
        _settings = dict(lda_form.value, seed=seed_picker.value)
        _same = [_l for _l, _r in model_history.items() if _r["settings"] == _settings]
        if _same:
            topic_model, ll_trace = model_history[_same[0]]["model"], model_history[_same[0]]["trace"]
            _out = mo.md(f"Switched to **{_same[0]}**. These settings and this seed were already trained, so nothing ran again.")
        else:
            topic_model, ll_trace = train_lda(**_settings)
            _label = f"run {len(model_history) + 1}: " + " ".join(f"{_key}={_val}" for _key, _val in _settings.items())
            model_history[_label] = {"settings": _settings, "model": topic_model, "trace": ll_trace}
            _row = {
                "session started": SESSION_STARTED,
                "trained at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                **history_row(_label, model_history[_label]),
                "log-likelihood/word trace (step:value)": " ".join(f"{_t[0]}:{_t[1]:.3f}" for _t in ll_trace),
            }
            pd.DataFrame([_row]).to_csv(HISTORY_CSV, mode="a", header=not HISTORY_CSV.exists(), index=False)
            _out = mo.md(
                f"Trained **{_label}** in {ll_trace[-1][0]} steps. "
                f"Kept {len(topic_model.used_vocabs):,} distinct tokens; removed as top words: `{list(topic_model.removed_top_words)}`. "
                f"Appended to `{HISTORY_CSV.name}`."
            )
    _out
    return (topic_model,)


@app.cell
def _(show_topics, topic_model):
    mo.stop(topic_model is None, mo.md("_Train a model with the form above to see its topics here._"))
    show_topics(topic_model)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Model History Table (Saved automatically; you will submit this with your assignment!!)

    Every run is automatically appended to `model_history.csv` next to this notebook as soon as it finishes training.

    It is okay if there are duplicate entries! (e.g. completing the homework across multiple sittings such that your local `model_history.csv` essentially appended multiple in-session tables)

    We will use these tables in-class activity after Assignment 1 is due!
    """)
    return


@app.cell
def _(HISTORY_CSV, history_row, model_history, topic_model):
    # Rows come from history_row (shared with the CSV append in the training cell); the "active"
    # column and the caption with the CSV path are added here. Same columns as before.
    mo.stop(not model_history, mo.md("_`model_history` is empty. Train a model with the form above._"))
    _rows = [{**history_row(_label, _run), "active": "*" if _run["model"] is topic_model else ""} for _label, _run in model_history.items()]
    mo.vstack([
        mo.ui.table(_rows, selection=None, pagination=False),
        mo.md(f"_Every run in this table was appended to `{HISTORY_CSV}` the moment it finished training. That file keeps the runs from earlier sittings too, and it is what you submit._"),
    ])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The plot below shows log-likelihood per word after every 100 steps for every model in `model_history`. You will want it for Question 6.

    Recall the caveat under `topic_model_v2`: log-likelihood per word is only comparable between runs with the same `min_cf`, `min_df`, and `rm_top` (check the "tokens kept" column). Curve shapes can be compared across runs, but values should be taken as a grain of salt.
    """)
    return


@app.cell
def _(model_history, topic_model):
    _ = topic_model   # read so that this cell re-runs after every form run (model_history changes in place)
    mo.stop(not model_history, mo.md("_Train a model with the form above to see its training curve._"))
    _fig, _ax = plt.subplots(figsize=(7, 3.5))
    for _label, _run in model_history.items():
        _ax.plot(
            [_t[0] for _t in _run["trace"]],
            [_t[1] for _t in _run["trace"]],
            marker=".",
            label=_label.split(":")[0] + f" (k={_run['settings']['k']}, seed={_run['settings']['seed']}, iters={_run['settings']['iters']})",
        )
    _ax.set_xlabel("training steps")
    _ax.set_ylabel("log-likelihood per word")
    _ax.legend(fontsize=7)
    _fig
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Two more helpers, for Questions 8 and 9. `coherence_score` wraps tomotopy's coherence metrics (higher is more coherent for every metric it offers; `u_mass` is always at or below 0); the aside before Question 9 shows it in action. `topic_by_newsgroup` counts, for each newsgroup, how many of its documents have each topic as their single most probable topic. Documents whose every token was pruned are skipped (their distribution would just be the prior). Both work as written on any model trained on `tokenized_docs`; for `topic_model_v4` (Question 7) pass `indices=kept_indices_v2`, because it was trained on a different list of documents.
    """)
    return


@app.function
# coherence helper (Question 8 plumbing)
def coherence_score(model, metric="c_v", top_n=10):
    """Mean coherence over all topics, computed on the model's own documents.
    metric: "c_v", "c_npmi", "c_uci", or "u_mass". Higher = more coherent for all four.
    Caveat: the score depends on the vocabulary the model kept, so two models with different
    thresholds are not on exactly the same scale."""
    return Coherence(model, coherence=metric, top_n=top_n).get_score()


@app.cell
def _(kept_indices, newsgroups_train):
    # dominant topic per document vs. true newsgroup (Question 8 plumbing)
    def topic_by_newsgroup(model, indices=None):
        """Rows: newsgroup. Columns: topic id. Cell: number of that newsgroup's documents whose single
        most probable topic is that column. `indices` maps model doc j -> newsgroups_train row; it
        defaults to kept_indices, which is correct for every model trained on tokenized_docs.
        For a model trained on other documents (topic_model_v4) pass its own index map (kept_indices_v2).
        Documents with no kept tokens are skipped: their topic distribution is just the prior."""
        indices = kept_indices if indices is None else indices
        if len(indices) != len(model.docs):
            raise ValueError(
                f"this model has {len(model.docs)} documents but indices has {len(indices)} entries; "
                "for topic_model_v4 pass indices=kept_indices_v2"
            )
        all_labels = newsgroups_train["label_text"]
        labels, dominant = [], []
        for i, doc in zip(indices, model.docs):
            if (doc.topics == -1).all():   # every token pruned by min_cf / min_df / rm_top
                continue
            dist = doc.get_topic_dist()
            labels.append(all_labels[i])
            dominant.append(max(range(len(dist)), key=lambda t: dist[t]))
        return pd.crosstab(pd.Series(labels, name="newsgroup"), pd.Series(dominant, name="dominant topic"))

    return


@app.cell
def _():
    # examples of the two helpers, commented out because coherence takes a few seconds
    # coherence_score(basic_topic_model), coherence_score(topic_model_v2)
    # topic_by_newsgroup(topic_model_v3)
    # topic_by_newsgroup(topic_model_v4, indices=kept_indices_v2)   # v4 needs its own index map
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 4: Varying k

    **Using the form above, train at least three models that differ only in k (for example 5, 20, and 50) and describe what changes.** Answer in ~3 sentences. Type your Question 2 thresholds into the form first, then keep them, the active seed, alpha, and eta fixed, so that k is the only difference. The `model_history` table keeps every run, and the model picker in "Viewing document topics" lets you look inside any of them.

    Report your other parameters' values! You do not strictly need to keep the defaults for them

    Some ideas and examples to get you started: "at k=5 the topics were basically newsgroup categories, at k=50 they split into \_\_\_\_\_" or "the topics that make no sense don't go away, there are just more of them" or "the topic about \_\_\_\_\_ showed up at every k with almost the same top words"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_4 = rf"""
    {PLACEHOLDER}
    """
    return (answer_4,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 5: Varying alpha and eta

    **Before you touch any sliders on the form above,** write down for yourself what you expect a larger alpha to do to one document's topic distribution, and a larger eta to one topic's top words.**

    **Then tick "Fix alpha" in the form** and play with the alpha slider on its own for a few runs, then the eta slider on its own, and **jot down some casual notes on what you see.** (1-2 sentences' equivalent) By the time you move onto the next step, you should have some idea of how much you should change the values of alpha and eta in order to see a difference.

    **Finally pick 2 combinations of alpha and eta** that would give you substantially different topics. Use the same values for all other parameters, and write about your observations. Answer this part in ~2-3 sentences: what you expected, what the 2 configurations did to the topics and to the per-document topic distributions, whether expectations matched observations, etc.

    Why the "Fix alpha" box: tomotopy re-estimates alpha every 10 steps by default, so without it the alpha you set is only a starting value, and `basic_topic_model`'s `summary()` above shows how far its per-topic alphas moved from 0.1. With the box ticked, `topic_model.alpha` stays at your value.

    Again, report your other parameters' values! You do not strictly need to keep the defaults for them

    Some ideas and examples to get you started: "with alpha=X every document was spread over many topics, while with alpha=Y most documents were one topic" or "raising eta made the top words \_\_\_\_\_" or "I expected \_\_\_\_\_ from lecture and it did / did not happen"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_5 = rf"""
    {PLACEHOLDER}
    """
    return (answer_5,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 6: Training for more and less

    Train one model for many steps (for example 3000) and look at its training curve. About where does log-likelihood per word stop improving, and do the topics keep changing after that point? (~2 sentences)

    Train a 200-step run and compare. Discuss noticeable differences between the topics they generated (~2 sentences)

    In general, how much do you observe you need to train to get good topics? (~1 sentence)

    Do you have any guesses about whether "how much to train" might be dependent on hyperparameter settings? Pick one hypothesis and test it. What do you observe ( ~3 sentences)

    Again, except for in the last part, everything else the same and remember to report your training configurations!

    Some ideas and examples to get you started: "the curve flattened around step \_\_\_\_\_ but topic \_\_\_\_\_ kept drifting" or "200 steps already gave me the same topics as 3000" or "the log-likelihood was still going up at 3000, so I'm not sure I trained long enough"

    **NOTE:** For some aspects of this question, you may want to write and use a helper function that does something different from the standard `train_lda()`-- you could print extra information from inside this helper function, or return it and handle it separately afterwards. Tou may need to adapt this invocation block here too (ctrl+c, ctrl+f a snippet to find the relevant cell), and/or run it again. No worries if you have trouble getting these records into `model_history` like normal, but it would be good practice to try :)

    ```
        topic_model, ll_trace = train_lda(**_settings)
        _label = f"run {len(model_history) + 1}: " + " ".join(f"{_key}={_val}" for _key, _val in _settings.items())
        model_history[_label] = {"settings": _settings, "model": topic_model, "trace": ll_trace}
        _row = {
            "session started": SESSION_STARTED,
            "trained at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            **history_row(_label, model_history[_label]),
            "log-likelihood/word trace (step:value)": " ".join(f"{_t[0]}:{_t[1]:.3f}" for _t in ll_trace),
        }
        pd.DataFrame([_row]).to_csv(HISTORY_CSV, mode="a", header=not HISTORY_CSV.exists(), index=False)
        _out = mo.md(
            f"Trained **{_label}** in {ll_trace[-1][0]} steps. "
            f"Kept {len(topic_model.used_vocabs):,} distinct tokens; removed as top words: `{list(topic_model.removed_top_words)}`. "
            f"Appended to `{HISTORY_CSV.name}`."
        )
    ```
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_6 = rf"""
    {PLACEHOLDER}
    """
    return (answer_6,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 7: Preprocessing before the model

    The thresholds set in the `LDAModel` as in Question 2 only affect frequency-based aspects of preprocessing. For all of our models so far, we are using the same pre-tokenization and tokenization set by the same `CountVectorizer`. In this question, we will explore other preprocessing methods that can affect the topics seen in your text, such as capitalization, stop words, token pattern. Train `topic_model_v4` on the result, and compare it with `topic_model_v3`. Answer in ~3-4 sentences: what you changed, what guiding principles led you to change what you did, what it removed, and what it did to the topics.

    Two things to keep in mind: 1) make sure you copy your `topic_model_v3` thresholds into the `train_lda` call in the cell below, so that the `CountVectorizer` is the only change between v3 and v4. 2) `rm_top` removes the N most frequent tokens that are left *after* the `CountVectorizer` ran, so if you had kept stopwords but then remove them, the same N will drop different words-- please report what it removed! The new tokenizer may also empty out a different set of documents, which is why this quesiton keeps its own `kept_indices_v2`. The document viewer above only covers models trained on `tokenized_docs`; to look at `topic_model_v4` by newsgroup, use `topic_by_newsgroup(topic_model_v4, indices=kept_indices_v2)`.

    Some ideas and examples to get you started: "lowercasing merged 'The' and 'the', and I saw a new topic for \_\_\_\_\_ that I had not seen before" or "requiring 3+ letters per token killed the digit topics" or "after lowercasing plus stop words, rm_top at the same N started removing content words like 'people' and 'like', so I lowered it"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_7 = rf"""
    {PLACEHOLDER}
    """
    return (answer_7,)


@app.cell
def _(kept_indices, newsgroups_train, show_topics, train_lda, vectorizer):
    # TODO: change the CountVectorizer arguments, then re-run this cell.
    # Note: min_df / max_df on a CountVectorizer only apply during fit(); build_analyzer() ignores them.
    # Use the LDAModel thresholds (min_cf, min_df, rm_top) for frequency pruning, as in Question 2.
    vectorizer_v2 = CountVectorizer(
        strip_accents="unicode",
        lowercase=False,                 # <- try True
        stop_words=None,                 # <- try "english" (the list is lowercase, so it only removes "the", not "The", unless lowercase=True)
        token_pattern=r"(?u)\b\w+\b",    # <- e.g. r"(?u)\b[a-zA-Z]{3,}\b" keeps only alphabetic tokens of 3+ letters
        ngram_range=(1, 1),
        analyzer="word",
    )
    # nothing below runs until at least one argument differs from the original `vectorizer` (saves a model train on every open)
    mo.stop(
        vectorizer_v2.get_params() == vectorizer.get_params(),
        mo.md("_Change at least one `CountVectorizer` argument above, then this cell trains `topic_model_v4`._"),
    )
    _analyzer_v2 = vectorizer_v2.build_analyzer()

    tokenized_docs_v2, kept_indices_v2 = [], []   # a new analyzer can empty out different docs, so keep a new index map
    for _i, _text in enumerate(newsgroups_train["text"]):
        _doc = _analyzer_v2(_text)
        if _doc:
            tokenized_docs_v2.append(_doc)
            kept_indices_v2.append(_i)

    topic_model_v4, _trace_v4 = train_lda(
        min_cf=0, min_df=0, rm_top=0,    # <- first copy the three values from your topic_model_v3 cell, so that the CountVectorizer is the only change
        docs=tokenized_docs_v2,
    )
    print(
        f"{len(tokenized_docs_v2):,} non-empty docs (was {len(kept_indices):,} with the original CountVectorizer); "
        f"kept {len(topic_model_v4.used_vocabs):,} of {len(topic_model_v4.vocabs):,} distinct tokens; "
        f"removed as top words: {list(topic_model_v4.removed_top_words)}"
    )
    show_topics(topic_model_v4)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 8: How useful are the original news groups?

    **Pick a model you liked and consider its "quality" in two ways: your own impression based on the top words, and the `topic_by_newsgroup` table. Where do the two agree, and where do they disagree?** Answer in ~3 sentences. Make sure to report which model and report its configuration!

    Remember: If your favorite is `topic_model_v4`, pass `indices=kept_indices_v2` to `topic_by_newsgroup`.

    Some ideas and examples to get you started: "the \_\_\_\_\_ newsgroup maps almost entirely onto topic \_\_\_\_\_, but \_\_\_\_\_ and \_\_\_\_\_ share one topic" or "the topics that make no sense don't line up with any newsgroup" or "the most interesting topics did not line up with a newsgroup"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_8 = rf"""
    {PLACEHOLDER}
    """
    return (answer_8,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Aside: coherence metrics (more on this later)

    So far you have judged topics by reading them. There are also automatic scores that have been developed to help judge topics. A *coherence* metric gives each topic a number based on how often its top words occur together in the documents, and the model's score is the mean over topics. Higher means more coherent. We will come back to evaluation later in the course; for now this is optional, and you can mention it in Question 8 above if you find it helpful.

    The cell below scores `basic_topic_model` and `topic_model_v2` and lists the per-topic scores for `topic_model_v3` next to the top words. It runs only when you press the button and takes about 20 seconds. Before you trust the number, look at which topics score high. A topic made of "the", "of", "to", "and" can score very well, because those words occur together in almost every document. The score also depends on which tokens the model kept, so it is only comparable between models with the same thresholds, like perplexity.
    """)
    return


@app.cell
def _():
    coherence_button = mo.ui.run_button(label="Compute coherence (c_v) for basic_topic_model, topic_model_v2, topic_model_v3")
    coherence_button
    return (coherence_button,)


@app.cell
def _(basic_topic_model, coherence_button, topic_model_v2, topic_model_v3):
    mo.stop(not coherence_button.value, mo.md("_Press the button above to compute the scores._"))
    _lines = [
        f"- `basic_topic_model`: c_v = {coherence_score(basic_topic_model):.3f}",
        f"- `topic_model_v2` (min_df=5): c_v = {coherence_score(topic_model_v2):.3f}",
        f"- `topic_model_v3` (yours): c_v = {coherence_score(topic_model_v3):.3f}",
    ]
    _coh = Coherence(topic_model_v3, coherence="c_v", top_n=10)
    _rows = ["| topic | c_v | top words |", "|---|---|---|"]
    for _k in sorted(range(topic_model_v3.k), key=lambda _t: -_coh.get_score(topic_id=_t)):
        _rows.append(f"| {_k} | {_coh.get_score(topic_id=_k):.3f} | {', '.join(_w for _w, _p in topic_model_v3.get_topic_words(_k, top_n=10))} |")
    mo.vstack([mo.md("\n".join(_lines)), mo.md("Per-topic c_v for `topic_model_v3`, best first:"), mo.md("\n".join(_rows))])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Question 9: Goal-directed exploration

    **Pick one thing you want a topic model of this corpus to do (for example: give each of the five `comp.*` newsgroups its own topic, or isolate the gun-control debate), and use everything above to get as close as you can. Report what you tried, what worked, what did *not* work as well as you might have hoped, and what you would consider trying next.** Answer in ~5 sentences, and report the settings of your final model.

    Some ideas and examples to get you started: "I wanted one clean topic per newsgroup, so I set k=20 and \_\_\_\_\_" or "the \_\_\_\_\_ articles kept merging with \_\_\_\_\_ no matter what I did" or "nothing separated \_\_\_\_\_ from \_\_\_\_\_; I think this might be because \_\_\_\_\_"
    """)
    return


@app.cell
def _(PLACEHOLDER):
    answer_9 = rf"""
    {PLACEHOLDER}
    """
    return (answer_9,)


if __name__ == "__main__":
    app.run()
