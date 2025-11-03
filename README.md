# SEO Content Quality & Duplicate Detector

## 1. Project Overview
This project is an end-to-end machine learning pipeline that analyzes web content for SEO quality. It parses raw HTML, extracts NLP features (like readability and word count), detects near-duplicate content using TF-IDF and cosine similarity, and trains a classification model to score content quality. [cite_start]The project includes a mandatory Jupyter Notebook for the core analysis and an optional bonus Streamlit app for real-time, interactive analysis [cite: 7, 13, 16-21].

## 2. 🚀 Deployed Streamlit App
For a live demonstration, the real-time analysis tool is deployed on Streamlit Cloud:

**[https://seo-content-detector-2448540.streamlit.app/](https://seo-content-detector-2448540.streamlit.app/)**

## 3. Project Structure
[cite_start]The repository follows the required structure for the Streamlit bonus submission [cite: 161-179]:

```
seo-content-detector/
├── data/
│   ├── data.csv                  # Dataset with URLs and content
│   ├── extracted_content.csv     # Parsed and cleaned content
│   ├── features.csv             # Extracted features for analysis
│   └── duplicates.csv           # Identified duplicate pairs
├── notebooks/
│   └── seo_pipeline.ipynb       # Main analysis notebook
├── models/                      # Models/artifacts for the notebook
│   └── ...
├── streamlit_app/
│   ├── app.py                   # Main Streamlit application
│   ├── utils/
│   │   ├── parser.py           # HTML parsing utilities
│   │   ├── features.py         # Feature extraction
│   │   └── scorer.py           # Quality scoring and ML models
│   └── models/                  # Saved ML models/artifacts for the app
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation
```

## 4. Setup Instructions
To run this project locally, clone the repository and install the required dependencies.

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/seo-content-detector](https://github.com/your-username/seo-content-detector)
cd seo-content-detector

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Mac/Linux
.\venv\Scripts\activate   # On Windows

# 3. Install the required dependencies
pip install -r requirements.txt
```
You will also need to download the 'punkt' tokenizer from NLTK:

```python
import nltk
nltk.download('punkt')
```

## 5. Quick Start (Core Analysis)
[cite_start]The mandatory part of the assignment is the Jupyter Notebook, which contains the full end-to-end analysis[cite: 155].

```bash
# Start Jupyter Notebook
jupyter notebook notebooks/seo_pipeline.ipynb
```
Running all cells in this notebook will:
1.  Parse the raw HTML from `data/data.csv`.
2.  Engineer features and save them to `data/features.csv`.
3.  Identify duplicate pairs and save them to `data/duplicates.csv`.
4.  Train and compare models, saving the best one to the `models/` folder.

## 6. Key Decisions
* **HTML Parsing:** Used `BeautifulSoup` to parse HTML. To get clean text, common non-content tags (like `<nav>`, `<footer>`, `<script>`) were stripped before extracting text from the main body.
* **Feature Engineering:** Utilized `scikit-learn`'s `TfidfVectorizer` for keyword extraction and as the embedding for similarity[cite: 71]. `textstat` was used for the `flesch_reading_ease` score, a key predictive feature.
* **Similarity Threshold:** A `cosine_similarity` threshold of **0.80** was chosen to identify near-duplicates[cite: 79]. This is strict enough to find true copies without flagging articles that are merely on the same topic.
* **Model Selection:** Both a `RandomForestClassifier` and a `LogisticRegression` model were trained and compared. The **Random Forest was chosen** as the final model due to its significantly higher accuracy (90.5% vs. 76.2%) and its ability to handle non-linear relationships between features.

## 7. Results Summary
The final `RandomForestClassifier` model performed exceptionally well, validating the usefulness of the engineered features.

* **Model Performance:**
    * **Winning Model:** Random Forest (Accuracy: 90.5%)
    * **Baseline Model:** Word Count Rule (Accuracy: 47.6%)
    * The final model's F1-Score (Weighted Avg) was **0.90**.
* **Duplicate Detection:**
    * `[Enter number from your output]` duplicate pairs were found with >80% similarity.
* **Key Features:** Readability was the most important factor in predicting content quality, followed by word and sentence counts.
    1.  `flesch_reading_ease` (Importance: 0.508)
    2.  `word_count` (Importance: 0.262)
    3.  `sentence_count` (Importance: 0.231)

## 8. Limitations
* **Synthetic Labels:** The model is trained on synthetic labels based on simple rules (e.g., `word_count > 1500`) [cite: 98-99]. Real-world content quality is far more complex and would require human-labeled data to model accurately.
* **Static Parser:** The `BeautifulSoup` parser only reads the initial static HTML. It cannot parse content loaded dynamically with JavaScript, which would cause it to fail on many modern web apps.
* **Small Dataset:** The analysis was performed on a small dataset (60-70 rows)[cite: 43]. The model's strong performance, especially for the `High` quality class (which had a support of only 3 in the test set), may not generalize well to a larger, more diverse set of web pages.