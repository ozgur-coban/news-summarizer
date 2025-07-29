# 📰 News Summarization Ensemble Demo

## Overview

This project implements a **modular, multi-strategy news summarizer** using a fine-tuned BART-large-CNN model, trained on 60,000+ company news articles. The system generates not just one, but **many different candidate summaries** for each article, using eight distinct modules, each with its own summarization logic, prompting style, or reranking strategy.

The goal is to:
- Achieve robust, adaptable news summarization for long, diverse, real-world articles
- Give users (or downstream systems) a choice of summaries, maximizing quality and relevance
- Provide interpretable, transparent model behavior (each summary is labeled with its module and logic)
- Enable user-controlled, guided summarization via tags

---

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Detailed Module Logic](#detailed-module-logic)
    - [Input Preprocessing](#input-preprocessing-and-length-handling)
    - [Summary Generation Modules](#summary-generation-modules)
    - [Summary Deduplication and Output](#summary-deduplication-and-output)
- [User Control: Guiding Tags](#user-control-guiding-tags)
- [Setup & Installation](#setup--installation)
- [Notebook Usage Instructions](#notebook-usage-instructions)
- [Python Libraries Used and Their Roles](#python-libraries-used-and-their-roles)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Extending This System](#extending-this-system)
- [Contact](#contact)

---

## Features

- **Eight summary-generation modules**: Each employs a different strategy (beam search, sampling, guided prompts, keyword extraction, reranking).
- **Handles long articles**: Automatic chunking, summarization, and recombination.
- **User-guidable**: Accepts tags/topics to focus the summary.
- **Interactive notebook UI**: Choose articles and get summaries on demand.
- **Transparent logic**: All summaries are labeled with their generating module.
- **Ready for extension**: Add or swap modules as needed.

---

## System Architecture

### **Input → [Chunking if needed] → [All Modules] → Deduplication → List of summaries + labels**

1. **Input Text**: The article to summarize, as a string.
2. **Preprocessing/Chunking**: If the article exceeds the model’s token limit, it is split into overlapping chunks, summarized individually, then rejoined.
3. **Module Ensemble**: Each module processes the article (or its summary), producing 1–N candidate summaries.
4. **Deduplication**: All generated summaries are deduplicated (exact matches are collapsed) and labeled with the module that created them.
5. **Output**: A list of `(summary, module_name)` pairs, ready for display or downstream selection.

---

## Detailed Module Logic

### Input Preprocessing and Length Handling

- **Why?**  
  Transformers like BART have a maximum context (e.g., 1024 tokens). News articles can exceed this, especially in business domains.
- **How?**  
  - The code checks if the input is too long for the model.
  - If so, it splits it into overlapping chunks (`max_chunk_tokens`, `overlap`).
  - Each chunk is summarized independently.
  - All chunk summaries are concatenated to form a single, coherent summary (used in downstream generation if needed).

### Summary Generation Modules

**Each module is implemented as a Python function, using specific logic:**

#### **Module 1: Baseline Generation**
- **Logic**: Generates a factual summary with beam search and a creative one with sampling.
- **Purpose**: Provides both a “safe” deterministic summary and a more varied/creative baseline.
- **Params**: `beam_search_params`, `sampling_params`.

#### **Module 2: Simple Prompters**
- **Logic**: Runs two prompt styles:  
    - A “simple command” prompt (“Summarize this article in one concise sentence”)
    - A “chain of thought” prompt (“Identify key entities/events, then summarize”)
- **Purpose**: See how direct vs. reasoning-based prompts affect results.

#### **Module 3: Metadata-Guided Summarizers**
- **Logic**:  
    - User provides tags/topics.
    - Module prompts the model to **focus the summary on those tags**.
    - Both beam search and sampling outputs are generated.
- **Purpose**: User- or application-steerable summarization.

#### **Module 4: Angled Summarizers**
- **Logic**:  
    - Produces a general summary (beam and sample)
    - For each tag, produces a focused “angle” summary (“summarize with focus on TAG”)
- **Purpose**: Useful for articles with multiple news angles.

#### **Module 5: Beam + Multiple Sampling Options**
- **Logic**:  
    - One high-confidence (beam) summary
    - Several creative samples, each generated in isolation (to maximize diversity)
- **Purpose**: Exposes the creative range of the model.

#### **Module 6: Automated Keyword-Guided Summarizers (YAKE)**
- **Logic**:  
    - Uses YAKE to extract important keywords/topics from the article.
    - Prompts the model to summarize **with explicit attention to those topics**.
    - Both beam and sample outputs.
- **Purpose**: Automatic focus on key info, without user needing to provide tags.

#### **Module 7: Keyword-Based Reranker (Simple Count)**
- **Logic**:  
    - Generates a pool of creative candidates (sampling).
    - Uses spaCy NER to extract entities/topics from the article.
    - Reranks candidates by **how many entities they mention**.
    - Returns only the best candidate.
- **Purpose**: Selects for summaries with strong factual coverage.

#### **Module 8: Weighted Keyword Reranker**
- **Logic**:  
    - Like Module 7, but each entity/topic is weighted by frequency in the article.
    - Scores summaries by **total entity weight covered**.
    - Returns the best candidate.
- **Purpose**: Prioritizes coverage of the main actors/topics.

### Summary Deduplication and Output

- All generated summaries from all modules are collected.
- Exact duplicates are removed.
- Each summary is returned with the module name that produced it.
- The final result is a **list of unique (summary, module label) pairs** for the input article.

---

## User Control: Guiding Tags

- The variable `GUIDING_TAGS` can be set by the user (as a Python list).
- Tags are used in Modules 3 and 4 to guide the summarizer.
- Example:
    ```python
    GUIDING_TAGS = ["Turkey", "Ukraine", "ceasefire"]
    ```
- Tags can be topics, entities, or custom keywords—whatever the user wants the summary to focus on.

---

## Setup & Installation

### Model Weights Setup

- **No manual download/upload required!**
- The notebook will **automatically copy** the model zip from a public Google Drive link directly into your Drive and unzip it to the correct folder.
- What to do:
    1. Run the notebook’s setup cells.
    2. Authenticate Google Drive when prompted.
    3. The script will:
        - Create `My Drive/models/` if needed.
        - Download and unzip the model as `bart-english-news-summarizer`.
    4. If the file already exists, the notebook will skip re-downloading.

### Python Dependencies

These will be auto-installed in Colab, but for standalone use:

```bash
pip install transformers sentencepiece torch accelerate
pip install spacy yake
pip install rouge_score evaluate
python -m spacy download en_core_web_sm
```

---

## Notebook Usage Instructions

1. **Run setup and model download/unzip cells.**
2. **Select or paste a news article** (via dropdown or by setting `INPUT_TEXT`).
3. **(Optional) Set `GUIDING_TAGS`** to focus the summary.
4. **Run the summarization cell** (`run_model_inference(INPUT_TEXT)`).
5. **Browse outputs**:
    - All generated summaries are shown with their corresponding module.
    - Use this pool for analysis, human selection, or further reranking.

---

## Python Libraries Used and Their Roles

- `transformers` (HuggingFace): Model loading, tokenization, summarization pipeline.
- `torch`: PyTorch backend for BART.
- `sentencepiece`: Tokenization for BART.
- `spacy`: For Named Entity Recognition (NER) and reranking logic.
- `yake`: Unsupervised keyword extraction for module 6.
- `math`, `time`, `collections.Counter`, `re`: Utilities for chunking, timing, scoring, and string handling.
- `rouge_score`, `evaluate`: For optional summary quality evaluation.
- `ipywidgets`, `IPython.display`: For interactive UI (if using in notebook).

---

## Troubleshooting & FAQ

**Q: Article too long?**  
A: The code splits it into manageable chunks, summarizes, and combines.

**Q: How do I use tags?**  
A: Set `GUIDING_TAGS` before running summarization. Used in Modules 3 and 4.

**Q: Model/file not found?**  
A: Ensure you run the notebook setup cell to download/copy the model weights.

**Q: Running outside Colab?**  
A: Install dependencies and update any paths as needed.

**Q: Can I add my own module?**  
A: Yes! Use the same pattern: write a function taking `(input_text, ...)`, add your logic, and plug into the ensemble.

---

## Extending This System

- **Add more modules**: For new prompts, models, or rerankers.
- **Replace the backbone model**: Swap out for other summarization models as needed.
- **Use other evaluation metrics**: ROUGE, BERTScore, or your own criteria.
- **Plug into an API or app**: Export the ensemble as a REST endpoint, Gradio demo, or internal tool.

---

## Contact

For questions, feedback, or collaboration, contact:  
**[Your Name]**  
[Your Email]  
[Your LinkedIn or GitHub]  

---

*This system was developed in a real-world ML internship context for enterprise news summarization, balancing engineering, research, and practical usability.*
