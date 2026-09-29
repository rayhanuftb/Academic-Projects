# Natural Language Processing (NLP) Analysis

**Course:** Big Data and Analytics in Education Lab (ICTE 4434)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

This project implements an end-to-end **Natural Language Processing (NLP)** analytics pipeline tailored for educational text mining. It extracts, preprocesses, analyzes, and visualizes student feedback, course evaluations, and discussion forum comments to provide actionable learning analytics.

---

## 🎯 Key Objectives

1. **Text Preprocessing**: Sanitize raw educational feedback text by stripping HTML tags, URLs, special characters, and converting text to lower case.
2. **Tokenization & Stop-Word Filtering**: Segment text into word tokens and remove standard English stopwords with support for Porter Stemming.
3. **N-Gram Analysis**: Extract unigram, bigram, and trigram sequences to detect recurring multi-word educational feedback themes (e.g., *"learning analytics"*, *"time series"*).
4. **Sentiment Polarity Scoring**: Assess student sentiment using domain-weighted lexicon matching to classify feedback as **Positive**, **Neutral**, or **Negative**.
5. **Lexical Diversity Analysis**: Measure Type-Token Ratio (TTR) and vocabulary richness across feedback corpora.
6. **Data Visualization**: Generate exportable publication-ready charts including frequency bar graphs, n-gram breakdowns, and sentiment distribution pie charts.

---

## 🏗️ Architecture & Directory Structure

```
Natural Language Processing Analysis/
├── data/
│   └── student_course_feedback.csv   # Educational feedback sample dataset
├── outputs/                           # Generated charts and CSV reports
│   ├── word_frequency.png
│   ├── ngram_distribution.png
│   ├── sentiment_distribution.png
│   └── feedback_sentiment_analysis.csv
├── src/
│   ├── __init__.py
│   ├── preprocessor.py               # Text cleaning, tokenization, stop-word removal
│   ├── analyzer.py                   # Word frequencies, n-grams, sentiment, metrics
│   ├── visualizer.py                 # Matplotlib charting and export engine
│   └── pipeline.py                   # High-level pipeline orchestrator
├── tests/
│   └── test_nlp.py                   # Automated unit & integration tests
├── main.py                           # CLI entrypoint
├── requirements.txt
└── README.md
```

---

## 📊 Sample Dataset Description

The bundled dataset [`data/student_course_feedback.csv`](./data/student_course_feedback.csv) contains synthetic educational evaluation records modeled on realistic university course evaluation surveys across multiple computer science and educational technology subjects.

| Column | Type | Description |
|---|---|---|
| `id` | Integer | Unique feedback record identifier |
| `course` | String | Name of the enrolled academic course |
| `student_id` | String | Anonymized student identifier (e.g., `STD_101`) |
| `feedback` | String | Raw qualitative feedback text submitted by the student |
| `rating` | Integer | Course rating score (1 to 5 scale) |

*Note: All student identities and ratings in this dataset are synthetic for academic and demonstration purposes.*

---

## 🚀 Installation & Execution

### 1. Prerequisites
- Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline on Default Sample Dataset
```bash
python main.py
```

### 4. Run Analysis on a Custom File
```bash
python main.py --file path/to/your_dataset.csv --column feedback --output-dir outputs
```

### 5. Run Analysis on Single Text String
```bash
python main.py --text "The machine learning lab on predictive modeling was informative and engaging!"
```

---

## 🧪 Running Automated Tests

Run the test suite using `unittest` or `pytest`:

```bash
python -m unittest discover -s tests
```
or
```bash
pytest tests/test_nlp.py -v
```

---

## 📈 Sample Outputs

- **Word Frequency Plot:** [`outputs/word_frequency.png`](./outputs/word_frequency.png)
- **N-Gram Distribution:** [`outputs/ngram_distribution.png`](./outputs/ngram_distribution.png)
- **Sentiment Breakdown:** [`outputs/sentiment_distribution.png`](./outputs/sentiment_distribution.png)
- **Sentiment CSV Report:** [`outputs/feedback_sentiment_analysis.csv`](./outputs/feedback_sentiment_analysis.csv)
