# 📰 BART English News Summarizer for Anadolu Ajansı

This repository contains the full pipeline for **training, evaluating, and analyzing** a BART-based news summarization model built for **Anadolu Ajansı** on a large-scale, domain-specific dataset of news articles.

The model was trained on **100,000** Anadolu Ajansı articles, with **50,000** of them approved for public release.  
The goal is to produce **concise, high-quality summaries** suitable for newswire usage.

---
## 📊 Evaluation on Test Set

The table below shows **average scores across all test articles** comparing BERTScore-picked outputs vs ROUGE-L-picked outputs.

|                | berts_f1     | berts_precision | berts_recall | rouge1       | rougeL       | bleu         | meteor       |
|----------------|--------------|-----------------|--------------|--------------|--------------|--------------|--------------|
| **bertS pick** | 0.896151196  | 0.880494372     | 0.912829919  | 0.420760638  | 0.368872702  | 0.152196796  | 0.475370778  |
| **rougeL pick**| 0.893670182  | 0.877660382     | 0.910755551  | 0.426010749  | 0.380812119  | 0.155462975  | 0.480405404  |

You can also find all of the calculated test results in [Google Sheet](https://docs.google.com/spreadsheets/d/1YF5aBUunMOFllANsjRmI5fXQmlCaRYw8wmznnx3hFG8/edit?usp=sharing) 
---


## 🚀 Usage

This project is designed to be **run interactively** through the provided Jupyter notebooks in the [`notebooks/`](notebooks/) directory.

- **[1-training-script]([Train Script](https://colab.research.google.com/drive/1iBLrXfxXPNlhA4pp-imE_MAQTeTewVYW?usp=sharing))** – Data loading, cleaning, and train/validation/test split and training methods.  
- **[2-eda-demo]([EDA Demo](https://colab.research.google.com/drive/1JTdj23ICOsBy7ynm6sh2sTk6V8KuiY-h?usp=sharing))** – Demo visualization of EDA work.  
- **[3-evaluation-script]([Evaluation Script](https://colab.research.google.com/drive/1OLpxg4_SmpUia5ZbTy2Sf0qSrsz1ZWEK?usp=sharing))** – Runs the trained model on the **test dataset** and evaluates outputs with multiple metrics (ROUGE, BLEU, METEOR, BERTScore). Includes both **full execution** and **pre-computed results** for 1,000 articles.  
- **[4-model-demo]([Model Demo](https://colab.research.google.com/drive/1ffk2tEZkgh_HrqyU1mPAshe6anAJsYKT?usp=sharing))** – Demo model usage that allows custom inputs and pre-computed examples. 

📌 **Recommendation:** Open the notebooks in Google Colab for a ready-to-run environment. Each notebook contains setup instructions.

---

## 📂 Project Structure

```
.
├── docs/ # Documentation and project notes
├── notebooks/ # Jupyter notebooks for preprocessing, training, EDA, demo, and testing
├── src/ # Python modules (EDA, preprocessing, scraping)
│ ├── eda/
│ │ ├── __init__.py
│ │ └── ...
│ ├── preprocessing/
│ │ ├── __init__.py
│ │ └── ...
│ ├── scraping/
│ │ ├── __init__.py
│ │ └── ...
├── LICENSE
├── requirements.txt
├── setup.py
└── README.md
```

---
## 🧩 Ensemble Summary Generation Modules

The summarization pipeline uses **8 distinct modules**, each producing different styles or focuses of summaries.  
Candidates from all modules are deduplicated and evaluated to select the best output.

### **Module 1: Baseline Generation**
- **Logic**: Generates a factual summary with beam search and a creative one with sampling.
- **Purpose**: Provides both a “safe” deterministic summary and a more varied/creative baseline.
- **Params**: `beam_search_params`, `sampling_params`.

### **Module 2: Simple Prompters**
- **Logic**: Runs two prompt styles:  
    - A “simple command” prompt (“Summarize this article in one concise sentence”)  
    - A “chain of thought” prompt (“Identify key entities/events, then summarize”)
- **Purpose**: Compare direct vs. reasoning-based prompts.

### **Module 3: Metadata-Guided Summarizers**
- **Logic**: User provides tags/topics. The model focuses on those topics using both beam and sampling.
- **Purpose**: User- or application-steerable summarization.

### **Module 4: Angled Summarizers**
- **Logic**:  
    - Produces a general summary (beam and sample)  
    - For each tag, produces a focused “angle” summary (“summarize with focus on TAG”)
- **Purpose**: Useful for articles with multiple news angles.

### **Module 5: Beam + Multiple Sampling Options**
- **Logic**:  
    - One high-confidence (beam) summary  
    - Several creative samples generated independently
- **Purpose**: Exposes the model’s creative range.

### **Module 6: Automated Keyword-Guided Summarizers (YAKE)**
- **Logic**:  
    - Extracts keywords/topics via YAKE  
    - Prompts the model to focus on them (beam + sample)
- **Purpose**: Automatically focuses on key information without manual tags.

### **Module 7: Keyword-Based Reranker (Simple Count)**
- **Logic**:  
    - Generates multiple candidates via sampling  
    - Uses spaCy NER to extract entities and reranks by count
- **Purpose**: Selects summaries with strong factual coverage.

### **Module 8: Weighted Keyword Reranker**
- **Logic**:  
    - Like Module 7, but weights each entity/topic by frequency  
    - Scores summaries by total entity weight covered
- **Purpose**: Prioritizes coverage of the main actors/topics.

---



## 📦 Installation

You can install all dependencies with:

```bash
pip install -r requirements.txt
```

Or install as a package in editable mode:

```bash
pip install -e .
```

This will ensure both the Python modules in `src/` and all required libraries are available.

---

## 📚 Dataset

**Source:** Anadolu Ajansı internal news archive (English)

**Size:** 100,000 articles total
- 50,000 public release
- 50,000 internal only (not included here)


The public dataset is provided as a ZIP archive in the notebooks and can be automatically downloaded during preprocessing or evaluation.

---

## 📜 License

This project is licensed under the MIT License – see the LICENSE file for details.